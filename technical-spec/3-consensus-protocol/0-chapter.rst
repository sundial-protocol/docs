.. _h:consensus-protocol:

Consensus protocol
==================

This chapter describes Midgard’s L1 contract-based consensus protocol,
which establishes the canonical chain of valid blocks. It consists of
the following components:

-  The operator directory is an onchain data structure that tracks
   active, retired, and newly registered Midgard operators.

-  The scheduler is an onchain mechanism that assigns evenly sized time
   windows to operators on a rotating schedule.

-  The state queue is an onchain data structure that holds operators’
   committed block headers until they are merged into the confirmed
   state or disqualified by fraud proofs.

-  When operators aren’t committing blocks for a long time, the
   escape-hatch mechanism can be used to commit a non-optimistic block
   that includes transaction and withdrawal orders for which full
   compliance proofs have been verified on L1.

-  Computation threads facilitate the onchain validation of submitted
   fraud proofs, splitting it up into steps that fit within Cardano’s
   limits on transaction size, computation, and memory.

-  The fraud proof catalogue defines the universe of fraud proof
   verification procedures for which computation threads can be spawned
   to target a block header in the state queue.

-  A fraud proof token indicates that a computation thread has
   successfully concluded to verify a fraud proof about a block header
   in the state queue.

-  The Midgard hub oracle wires all the onchain components together by
   storing their minting policy IDs and spending validator addresses for
   easy reference.
