.. _h:data-availability-layer:

Data availability layer
=======================

The data availability layer is critical to Midgard’s security because
every committed block needs to be publicly available throughout the
maturity period so that watchers can detect and prove fraud before
invalid blocks are merged.

We are considering three solutions for the data availability layer (in
decreasing preference):

#. Cardano Leios blobs (the ideal solution)

#. Multi-signature committees

.. _h:data-availability-leios:

Data availability via Leios blobs
---------------------------------

The ideal data availability solution for Midgard is based on Cardano
Leios blobs, which are a proposed feature in Cardano that will support
large-scale transient data storage secured via L1 consensus.

The contents of these blobs do not have to be verified by Cardano’s
Ouroboros consensus protocol, and they only have to be stored for up to
30 days. This means that a large amount of data can be stored in these
blobs sustainably for a low cost, which we expect to be several orders
of magnitude lower than Cardano’s cost for transaction metadata (which
is stored permanently).

Leios blobs are a natural intermediate point on Leios’ multi-year
roadmap toward full input-endorser capabilities. We believe that they
are achievable before Midgard’s planned deployment on mainnet, and we
will support the Leios team to help bring them to Cardano sooner.

In the Leios-based data availability solution for Midgard, operators
will pay to store their full non-Merkelized blocks inside Leios blobs
for the full maturity period. Leios itself will provide timestamps and
(non-Merkle) hashes for the blobs and ensure that the blob contents are
accessible. Midgard’s L1 smart contracts will be able to access the
timestamps and non-Merkle hashes of blobs directly.

The block data inside each Leios blob will be sufficient to be converted
offchain into the Merkelized representation of Midgard blocks that is
necessary to construct fraud proofs. The correspondence between the
non-Merkelized block data stored in the Leios blob and the Merkle root
hash declared in the block header will be verifiable via a special fraud
proof verification procedure. This procedure will calculate the Merkle
root hash in a streaming fashion over the block data and compare it to
the declared Merkle root hash in the block header.

Operators’ costs for storing blocks in Leios will be offset by the
revenue they collect from Midgard transaction, deposit, and withdrawal
fees. Furthermore, the Leios blob storage fees will become an additional
source of revenue for Cardano L1 block producing nodes, further boosting
the economic security of Cardano L1 on which Midgard depends.

.. _h:data-availability-multisig:

Data availability via Mithril
-----------------------------

If Leios blobs are unavailable on Cardano mainnet in time for Midgard’s
deployment, a viable alternative is using stake-weighted Mithril
certificates to ensure data availability.

The Mithril whitepaper states that it was specifically designed to
address the data-availability problem:

Mithril provides an immediate solution to the data-availability problem:
if the underlying consensus protocol is run on references for which a
Mithril signature exists, data availability is (cryptographically)
guaranteed.

In this approach, a state commitment is only considered valid if it is
accompanied by a Mithril certificate signed by a stake-weighted quorum
of Mithril participants. This certificate represents the Mithril
participants’ collective claim that the necessary block data is publicly
available.

Midgard’s L1 consensus protocol is adapted as follows:

#. **Publishing Data:** When the current operator wishes to commit a new
   block header to the state queue, they must publish the block’s full
   data at a publicly accessible location. This data must be sufficient
   to reconstruct the Merkle roots referenced by the block header.

#. **Verification by Mithril Participants:** Each Mithril participant
   monitors the publicly accessible location. When a new block is
   published, the Mithril participant independently retrieves the
   block’s data and verifies that:

   -  The data is available.

   -  It corresponds exactly to the Merkle roots in the state
      commitment.

#. **Signing the Certificate:** If the block’s data meets these
   conditions, the Mithril participant signs the Mithril certificate and
   broadcasts the signature to the Mithril aggregators.

#. **Onchain Verification:** The Midgard state queue requires every new
   block header to be appended with an associated Mithril certificate
   signed by Midgard’s quorum for the Mithril-based DA. Midgard’s
   parameter sets this quorum threshold.

By leveraging Mithril, Midgard ensures that state commitments are only
accepted when their corresponding block data is provably available. This
mechanism safeguards Midgard against data-availability fraud, where a
malicious operator attempts to submit a state commitment without
disclosing the underlying data. Without access to this data, fraud
provers would be unable to construct and submit fraud proofs, allowing
the fraudulent state commitment to become canonical once the fraud
detection window closes. By requiring a Mithril certificate before a
state commitment is appended, Midgard guarantees that the data remains
accessible, preserving the system’s integrity.

A key difference between the Leios blob and Mithril-based data
availability (DA) solutions lies in the security guarantees each
approach provides. In the Leios blob solution, data availability is
assured with the full security of Cardano’s consensus, meaning that all
active stake on the network contributes to securing DA, just as it does
for transaction finality and block production. Thus, any attempt to
suppress or manipulate stored data would require an adversary to control
a majority of Cardano’s total stake, making attacks highly impractical.
In contrast, the Mithril-based DA solution relies on a subset of
Cardano’s stake—specifically, the stake controlled by SPOs (Stake Pool
Operators) running Mithril or, equivalently, the total stake actively
participating in Mithril. While this still provides strong cryptographic
guarantees, it does not benefit from the full economic security of
Cardano’s entire stake-weighted consensus, making it theoretically more
susceptible to adversarial control if a sufficiently large fraction of
the Mithril-active stake colludes or becomes compromised.

This difference in security between the Leios blob and Mithril-based
data availability (DA) solutions is alleviated as more SPOs participate
in Mithril. As the number of SPOs running Mithril nodes grows, an
increasing proportion of Cardano’s total stake becomes actively involved
in securing the DA, thereby increasing the overall economic security of
the Mithril-based approach. As Mithril approaches universal adoption
among Cardano’s SPOs, the Mithril-based DA solution’s resilience
converges to that of the Leios blob-based DA solution. At the limit,
they are equivalent because the same stake-weighted economic security
backs both.

Therefore, broad participation in Mithril among Cardano SPOs is key to
minimizing any security gap between the two approaches.
