.. _h:ledger-state:

Ledger state
============

Midgard’s L2 ledger consists of a chain of blocks. Each block defines a
transition from the previous block’s set of unspent transaction outputs
(utxos) to a new utxo set. Unlike Cardano’s closed-system L1 ledger,
Midgard’s open-system L2 ledger allows block transitions to create and
destroy utxos in response to exogenous events—namely, deposits and
withdrawal requests that occur on the L1 ledger. This is in addition to
Midgard’s endogenous L2 transactions, which work the same as L1
transactions but with reduced functionality (no staking/governance
actions). [1]_

The blocks are stored temporarily on Midgard’s data availability layer
and permanently on Midgard’s archive nodes. The blocks’ headers are
committed to Midgard’s L1 state queue data structure to establish
immutability for the blocks’ sequence and contents as part of Midgard’s
L1 contract-based consensus protocol. Block headers have a fixed byte
size regardless of how many deposit, transaction, and withdrawal events
are held by their blocks—this size leverage between blocks and headers
is how Midgard multiplies Cardano’s transaction throughput.

Midgard L1 contract-based consensus protocol irreversibly considers a
block to be confirmed as soon as all its predecessors are confirmed and
one of the following holds:

Optimistic confirmation.
   The block’s maturity period has elapsed without any fraud proof being
   verified on L1 to prove that the block violates one of Midgard’s
   ledger rules.

Non-optimistic confirmation.
   A compliance proof has been verified on L1 to prove that the block
   complies with all Midgard ledger rules.

The irreversibility of block confirmation allows the L1 representation
of confirmed block headers to be condensed. For instance, it can stop
tracking confirmed withdrawal requests after they are paid out and
confirmed deposits after they are absorbed into Midgard’s reserve. It
can avoid tracking any confirmed transactions and only needs to track
the last confirmed block’s utxo set, as it is required to confirm the
next block. Finally, it can drop all other header data for the last
confirmed block’s predecessors, as it is implicitly tracked by a chained
hash in the last confirmed header and is not required to confirm the
next block.

As a result, Midgard’s L1 confirmed state consists of a fixed-byte-size
record with selected fields from the last confirmed block header and a
variable-size dataset tracking confirmed withdrawal requests and
deposits until they are processed.

.. [1]
   Cardano developers concerned about the absence of the “Withdraw 0”
   action need not worry. Midgard’s ledger rules permit the “Observe”
   script purpose defined in
   `CIP-112 <https://github.com/cardano-foundation/CIPs/tree/master/CIP-0112>`__,
   which is a more principled replacement for “Withdraw 0” that is
   expected to arrive in the next era of Cardano mainnet in 2025.
