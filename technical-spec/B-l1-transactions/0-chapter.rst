.. _h:midgard-l1-transactions:

Midgard L1 transactions
=======================

This chapter specifies the L1 transactions that interact with Midgard’s
consensus protocol smart contracts. Whereas the onchain smart contract
are specified in a modular way, where each validator is only concerned
with its own validity conditions, the transactions specified in this
chapter often interact with several of the onchain validators and must
satisfy all of their conditions. In this way, the offchain code can be
seen as the integration layer for the onchain code.
