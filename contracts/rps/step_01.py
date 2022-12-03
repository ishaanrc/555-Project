from logging import log

from pyteal import *
from pyteal.ast.bytes import Bytes
from pyteal_helpers import program

global_public_key = Bytes("global_public_key")

def approval():
    # locals
    local_opponent = Bytes("opponent")  # byteslice
    local_wager = Bytes("wager")  # uint64
    local_commitment = Bytes("commitment")  # byteslice
    local_reveal = Bytes("reveal")  # byteslice
    local_done = Bytes("done")

    op_challenge = Bytes("challenge")
    op_reveal = Bytes("reveal")

    @Subroutine(TealType.none)
    def reset(account: Expr):
        return Seq(
            App.localPut(account, local_opponent, Bytes("")),
            App.localPut(account, local_wager, Bytes("")),
            App.localPut(account, local_commitment, Bytes("")),
            App.localPut(account, local_reveal, Bytes("")),
            App.globalPut(global_public_key, Bytes("")),
        )

    # @Subroutine(TealType.uint64)
    # def is_empty(account: Expr):
    #     return Return(
    #         And(
    #             App.localGet(account, local_opponent) == Bytes(""),
    #             App.localGet(account, local_wager) == Bytes(""),
    #             App.localGet(account, local_commitment) == Bytes(""),
    #             App.localGet(account, local_reveal) == Bytes(""),
    #         )
    #     )
    #
    # # @Subroutine(TealType.uint64)
    # # def is_valid_play(p: Expr):
    # #     first_letter = ScratchVar(TealType.bytes)
    # #     return Seq(
    # #         first_letter.store(Substring(p, Int(0), Int(1))),
    # #         Return(
    # #             Or(
    # #                 first_letter.load() == Bytes("r"),
    # #                 first_letter.load() == Bytes("p"),
    # #                 first_letter.load() == Bytes("s"),
    # #             )
    # #         ),
    # #     )
    #
    @Subroutine(TealType.none)
    def create_challenge():
        App.globalPut(global_public_key, Txn.application_args[1]),
        return Seq(
            # basic sanity checks
            program.check_self(
                group_size=Int(2),
                group_index=Int(0),
            ),
            program.check_rekey_zero(2),
            Assert(
                And(
                    # second transaction is wager payment
                    Gtxn[1].type_enum() == TxnType.Payment,
                    Gtxn[1].receiver() == Global.current_application_address(),
                    Gtxn[1].close_remainder_to() == Global.zero_address(),
                    # second account has opted-in
                    App.optedIn(Int(1), Int(0)),
                    # is_empty(Int(1)),
                    # is_empty(Int(2)),
                    # is_empty(Int(0)),
                    # commitment
                    Txn.application_args.length() == Int(2),
                )
            ),
            App.localPut(Txn.sender(), local_opponent, Txn.accounts[2]),
            App.localPut(Txn.sender(), local_wager, Gtxn[1].amount()),
            App.localPut(
                Txn.sender(),
                local_commitment,
                Txn.application_args[1],
            ),
            Approve(),
        )

    @Subroutine(TealType.none)
    def accept_challenge():
        return Seq(
            # basic sanity checks
            program.check_self(
                group_size=Int(2),
                group_index=Int(0),
            ),
            program.check_rekey_zero(2),
            Assert(
                And(
                    # second (opponent) account has opted-in
                    App.optedIn(Int(2), Int(0)),
                    # second account has challenged this account
                    App.localGet(Int(2), local_opponent) == Txn.sender(),
                    # second transaction is wager match
                    Gtxn[2].type_enum() == TxnType.Payment,
                    Gtxn[2].receiver() == Global.current_application_address(),
                    Gtxn[2].close_remainder_to() == Global.zero_address(),
                    Gtxn[2].amount() == App.localGet(Int(2), local_wager),
                    # no commitment on accept, just instant reveal
                    Txn.application_args.length() == Int(2),
                    # is_valid_play(Txn.application_args[1]),
                )
            ),
            App.localPut(Int(2), local_opponent, Txn.accounts[1]),
            App.localPut(Int(1), local_wager, Gtxn[1].amount()),
            App.localPut(Int(1), local_reveal, Txn.application_args[1]),
            App.localPut(Int(2), local_done, Txn.application_args[1]),
            Approve(),
        )

    #
    # @Subroutine(TealType.uint64)
    # def winner_account_index(play: Expr, opponent_play: Expr):
    #     return Return(
    #         Cond(
    #             [play == opponent_play, Int(2)],  # tie
    #             [(play + Int(1)) % Int(3) == opponent_play, Int(1)],  # opponent wins
    #             [
    #                 (opponent_play + Int(1)) % Int(3) == play,
    #                 Int(0),
    #             ],  # current account win
    #         )
    #     )

    @Subroutine(TealType.none)
    def send_reward(account_index: Expr, amount: Expr):
        return Seq(
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields(
                {
                    TxnField.type_enum: TxnType.Payment,
                    TxnField.receiver: Txn.accounts[account_index],
                    TxnField.amount: amount,
                }
            ),
            InnerTxnBuilder.Submit(),
        )

    @Subroutine(TealType.none)
    def reveal():
        # winner = ScratchVar()
        # wager = ScratchVar()
        # return Seq (
        #     # basic sanity checks
        #     program.check_self(
        #         group_size=Int(1),
        #         group_index=Int(0),
        #     ),
        #     program.check_rekey_zero(1),
        #     Assert(
        #         And(
        #             # verify game data matches
        #             App.localGet(Int(0), local_opponent) == Txn.accounts[1],
        #             App.localGet(Int(1), local_opponent) == Txn.sender(),
        #             App.localGet(Int(0), local_wager)
        #             == App.localGet(Int(1), local_wager),
        #             # this account has commitment
        #             App.localGet(Int(0), local_commitment) != Bytes(""),
        #             # opponent account has a reveal
        #             App.localGet(Int(1), local_reveal) != Bytes(""),
        #             # require reveal argument
        #             Txn.application_args.length() == Int(2),
        #             # validate reveal
        #             Sha256(Txn.application_args[1])
        #             == App.localGet(Int(0), local_commitment),
        #         )
        #     ),
        #     wager.store(App.localGet(Int(0), local_wager)),
        #     # winner.store(
        #     #     # winner_account_index(
        #     #     #     play_value(Txn.application_args[1]),
        #     #     #     play_value(App.localGet(Int(1), local_reveal)),
        #     #     # )
        #     # ),
        #     If(winner.load() == Int(2))
        #     .Then(
        return Seq(
            # tie: refund wager to each party
            send_reward(Int(2), Int(0)),
            reset(Int(0)),
            reset(Int(1)),
            Approve(),
        )
        # )
        # .Else(
        #     # send double wager to winner
        #     send_reward(winner.load(), wager.load() * Int(2))
        # ),

        # )

    return program.event(
        init=Approve(),
        opt_in=Seq(
            reset(Int(0)),
            Approve(),
        ),
        no_op=Seq(
            Cond(
                [
                    Txn.application_args[0] == op_challenge,
                    create_challenge(),
                ],

                [
                    Txn.application_args[0] == op_reveal,
                    reveal(),
                ],
            ),
            Reject(),
        ),
    )

def clear():
    return Approve()
