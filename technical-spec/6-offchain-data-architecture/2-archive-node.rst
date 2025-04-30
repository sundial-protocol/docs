.. _h:archive-node:

Archive node
============

Midgard’s archive nodes will store the block data for confirmed blocks.
Security properties are easier to achieve for this historical data
because, at all times, Midgard’s confirmed state utxo contains a chained
header hash that pins the entire historical chain of confirmed blocks.
There can be no disagreement about different versions of this data—an
archive node either stores data that corresponds to the confirmed state
header hash, or it does not.

We expect all operators to keep a copy of the latest confirmed block’s
utxo set because it is necessary for them to create honest blocks and
avoid being slashed for fraudulent blocks. They are incentivized to do
so by the fee revenue they earn on Midgard. This utxo set and the block
data stored in the data availability layer provide Midgard with the
minimum information necessary to continue producing blocks.

We expect indexers and other professional service providers to store
copies of the Midgard historical data. Midgard’s security and ongoing
block-production capability does not depend on this historical data.
However, we expect it to be stored to the extent that users are willing
to pay for this service.
