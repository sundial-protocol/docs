.. _h:protocol-security:

Protocol security
=================

.. _h:malicious-majority-stake-attack:

Malicious majority stake attack
-------------------------------

A majority stake attack can allow the adversary to degrade the Liveness
and Finality security properties of a blockchain protocol, if the
adversary holds a sufficient percentage (e.g. 51%) of the network’s
primary resource (e.g. hashing power for Bitcoin, ADA for Cardano). In
practical terms, this attack can allow the adversary to revert recently
confirmed transactions and extract value from victims by preventing the
reverted transactions from being restored to the ledger.

Midgard’s consensus protocol is implemented entirely via Cardano L1
smart contracts. This means that an attack to revert any transaction
that evolves the state of these L1 smart contract is as difficult as an
attack against Cardano’s finality security property, against which
Cardano’s Ouroboros consensus protocol is highly resistant. In simpler
terms, Cardano’s full ADA supply on L1 is the resource against which a
majority stake attack must prevail to affect Midgard’s L2 ledger.

Furthermore, every L2 transaction in Midgard is only confirmed after two
consensus transactions occur on L1:

-  First, the L2 transaction is included in a block header committed to
   Midgard’s state queue.

-  Second, the block header is merged to Midgard’s confirmed state after
   waiting in the queue for the maturity period.

Both of the above L1 transactions must be reverted to revert a confirmed
L2 transaction in Midgard. Due to the mandatory maturity period between
the two L1 transactions, this amounts to a long-range attack to fork
Cardano’s blockchain before the maturity period began. However,
according to the Ouroboros consensus protocol, Cardano nodes will always
reject any forks that diverge from their local chain by more than 2160
blocks, which is approximately 12 hours (with very tight confidence
bounds). As Midgard’s maturity period protocol parameter will certainly
be longer than 24 hours (see
`[h:protocol-parameters] <#h:protocol-parameters>`__), it will be
impossible to revert both consensus transactions on L1 for a confirmed
L2 transaction on Midgard.

Suppose the adversary succeeds in an attack against Cardano’s finality
property, reverting the second consensus transaction for a Midgard L2
transaction. This reversion will restore the block header to the
beginning of the state queue, allowing it to be immediately re-merged to
Midgard’s confirmed state. Moreover, no conflicting block header can be
merged to the confirmed state in its place. Thus, the adversary’s attack
has no practical effect other than slightly delaying the inevitable
confirmation.

Suppose the adversary reverts the first consensus transaction for a
Midgard L2 transaction. This reversion will remove the block header from
the state queue. If the adversary is *not* colluding with the current
operator in Midgard, then the current operator will simply recommit the
block header to the state queue, nullifying any effects of the
adversary’s attack. If the adversary is colluding with the current
operator, then the adversary’s attack is redundant—the same effect is
achieved if the current operator abuses its power to censor L2
transactions. However, Midgard has safeguards in place against such
abuse (see `1.2 <#h:operator-abuse-of-power>`__).

.. _h:operator-abuse-of-power:

Operator abuse of power
-----------------------

Each operator has the exclusive privilege to commit blocks to the state
queue and resolve nodes in the settlement queue during their assigned
shifts (see `[h:time-model] <#h:time-model>`__), the duration of which
is controlled by the protocol parameter (see
`[h:protocol-parameters] <#h:protocol-parameters>`__). The current
operator has discretion over whether and when to commit blocks to the
state queue and the contents of those blocks. This discretion can be
abused to censor L2 transactions, but Midgard’s consensus protocol has
safeguards in place against such abuse.

Midgard deposits and withdrawals are initiated via L1 smart contracts
that assign definite inclusion times to them. An operator block is
invalid if it contains these inclusion times in its event interval but
fails to include the associated deposit or withdrawal events. This
ensures that if operators continue committing blocks to Midgard’s state
queue, then they cannot ignore deposit and withdrawal events.

Midgard L2 transaction requests are typically submitted to operators via
a publicly accessible API, and they can be ignored by operators.
However, any user can escalate his L2 transaction request by posting a
transaction order on L1. Similar to Midgard deposits and withdrawals, an
L1 transaction order is assigned an inclusion time that guarantees its
inclusion in a subsequent valid block.

If Midgard operators stop committing blocks at all to the state queue,
then the inclusion times on their own cannot guarantee that deposits,
withdrawals, and L2 transactions will be processed in a timely manner.
However, for this extreme case, Midgard’s consensus protocol includes
the escape hatch mechanism, which allows a special non-optimistic block
to be appended to the state queue by a non-operator. This block can
include any deposits, withdrawals, and L2 transactions that are verified
on L1 to comply with Midgard’s ledger rules. This ensures that user
funds cannot be stranded on Midgard even if its operators entirely stop
committing blocks.

.. _h:replay-attack:

Replay attack
-------------

In a replay attack, the adversary repeats or delays a valid message to
confuse the network and achieve a malicious outcome.

Midgard’s entire consensus protocol is implemented as a set of smart
contracts on Cardano L1 that evolve via L1 transactions. Each of these
L1 transactions must spend at least one utxo, which means that Cardano’s
ledger rule against double-spending utxos prevent these transactions
from being replayed.

However, Cardano’s ledger rules do not directly see the contents
corresponding to any hashes in the consensus protocol state on L1, such
as the utxos, L2 transactions, deposits, and withdrawals in a block
header. Nonetheless, Midgard has comprehensive ledger rules against the
various ways in which utxos, L2 transactions, deposits, and withdrawals
can be duplicated within a block or across blocks. Any operator that
commits a block header to the state queue that contravenes these ledger
rules forfeits his bond if the corresponding fraud proof is verified on
L1 within the block’s maturity period.

Another form of replay attack involves reusing the same confirmed
deposit or withdrawal event in the settlement queue to absorb more
deposited funds than necessary into Midgard’s reserve or release more
funds than necessary from it for a withdrawal. Midgard prevents this by
requiring an L1 utxo to be created on L1 for every deposit and
withdrawal, which must be spent whenever the corresponding deposit is
absorbed or withdrawal is paid out.
