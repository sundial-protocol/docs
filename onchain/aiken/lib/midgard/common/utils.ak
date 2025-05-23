use aiken/cbor
use aiken/collection/dict
use aiken/collection/list
use aiken/crypto.{
  ScriptHash, VerificationKey, VerificationKeyHash, blake2b_224, blake2b_256,
}
use aiken/interval.{Finite, Interval, NegativeInfinity, PositiveInfinity}
use aiken_design_patterns/validity_range_normalization as vrn
use cardano/address.{Address, Script}
use cardano/assets.{AssetName, PolicyId, Value, tokens}
use cardano/transaction.{Input, Output, OutputReference, ValidityRange}
use midgard/common/constants.{
  max_validity_range_for_current_time, posix_time_none,
}
use midgard/common/types.{H28, H32, PosixTime}

/// Check whether the interval starts on or after the point.
pub fn is_hereafter(self: Interval<Int>, point: Int) -> Bool {
  when self.lower_bound.bound_type is {
    Finite(lo) -> point <= lo
    NegativeInfinity -> False
    PositiveInfinity -> True
  }
}

/// Check whether the interval ends on or before the point.
pub fn is_herebefore(self: Interval<Int>, point: Int) -> Bool {
  when self.upper_bound.bound_type is {
    Finite(hi) -> hi <= point
    PositiveInfinity -> False
    NegativeInfinity -> True
  }
}

pub fn validate_mint(
  mints: Value,
  expected_minting_policy: ByteArray,
  expected_minting_name: ByteArray,
  expected_minting_amt: Int,
) -> Bool {
  let mints_policy = dict.to_pairs(tokens(mints, expected_minting_policy))
  mints_policy == [Pair(expected_minting_name, expected_minting_amt)]
}

pub fn safe_list_last(elems: List<a>) -> a {
  expect Some(last_elem) = list.last(elems)
  last_elem
}

pub fn safe_list_head(elems: List<a>) -> a {
  expect Some(last_elem) = list.head(elems)
  last_elem
}

pub fn safe_list_init(elems: List<a>) {
  expect Some(elems_except_last) = list.init(elems)
  elems_except_last
}

pub fn is_posix_time_none(time: PosixTime) {
  time == posix_time_none
}

/// Returns the quantity of all tokens with the policyId
pub fn quantity_of_policy_id(value: Value, policyId: PolicyId) {
  dict.foldl(tokens(value, policyId), 0, fn(_k, v, result) { v + result })
}

pub fn get_own_hash(output_reference: OutputReference, txInputs: List<Input>) {
  expect Some(input) =
    list.find(txInputs, fn(x) { x.output_reference == output_reference })

  expect Script(hash) = input.output.address.payment_credential
  hash
}

pub fn get_own_address(output_reference: OutputReference, txInputs: List<Input>) {
  expect Some(input) =
    list.find(txInputs, fn(x) { x.output_reference == output_reference })

  input.output.address
}

/// Helper function for accessing spending UTxO using its input index.
pub fn get_own_input_at(
  inputs: List<Input>,
  own_out_ref: OutputReference,
  input_index: Int,
) -> Output {
  expect Some(Input { output: own_utxo, output_reference: spent_own_out_ref }) =
    list.at(inputs, input_index)
  expect (own_out_ref == spent_own_out_ref)?
  own_utxo
}

pub fn is_output_to_sc(output: Output, scHash: ByteArray) -> Bool {
  when output.address.payment_credential is {
    Script(hash) -> hash == scHash
    _ -> False
  }
}

pub fn get_current_time(validity_range: ValidityRange) -> PosixTime {
  when vrn.normalize_time_range(validity_range) is {
    vrn.ClosedRange { lower, upper } -> {
      expect upper - lower <= max_validity_range_for_current_time
      upper
    }
    _ -> fail @"Unexpected validity range provided."
  }
}

pub fn has_signed(
  signer: VerificationKeyHash,
  extra_signatories: List<VerificationKeyHash>,
) -> Bool {
  extra_signatories |> list.has(signer)
}

pub fn get_single_asset_from_value_apart_from_ada(
  v: Value,
) -> (PolicyId, AssetName, Int) {
  expect [Pair(sym, tn_qty_pairs)] =
    v
      |> assets.to_dict
      |> dict.delete(assets.ada_policy_id)
      |> dict.to_pairs
  expect [Pair(tn, qty)] = tn_qty_pairs |> dict.to_pairs
  (sym, tn, qty)
}

/// For beacon UTxOs with specific policy IDs at a given address.
pub fn get_authentic_input_with_policy_at_address(
  inputs: List<Input>,
  address: Address,
  nft_policy_id: PolicyId,
  nft_token_name: ByteArray,
  input_index: Int,
) -> Input {
  expect Some(
    Input { output: Output { address: input_addr, value: input_value, .. }, .. } as found_input,
  ) = list.at(inputs, input_index)

  let input_nft_triplet =
    get_single_asset_from_value_apart_from_ada(input_value)

  expect and {
      input_addr == address,
      input_nft_triplet == (nft_policy_id, nft_token_name, 1),
    }

  found_input
}

/// For beacon UTxOs of validators which their NFTs have policy IDs equal to
/// their payment credentials.
pub fn get_authentic_input_of(
  inputs: List<Input>,
  address_script_hash: ScriptHash,
  nft_token_name: ByteArray,
  input_index: Int,
) -> Input {
  expect Some(
    Input {
      output: Output {
        address: Address { payment_credential: Script(refs_script_hash), .. },
        value: refs_value,
        ..
      },
      ..
    } as found_ref_input,
  ) = list.at(inputs, input_index)

  let refs_nft_triplet = get_single_asset_from_value_apart_from_ada(refs_value)

  expect and {
      refs_script_hash == address_script_hash,
      refs_nft_triplet == (address_script_hash, nft_token_name, 1),
    }

  found_ref_input
}

// Used to retrieve asset name from a value with a specific policy id
pub fn get_asset_name_from_value_with_policy(
  value: Value,
  policy_id: PolicyId,
) -> AssetName {
  expect [Pair(asset_name, _)] =
    value
      |> assets.tokens(policy_id) //return dict of policy id to asset name and quantity
      |> dict.to_pairs

  asset_name
}

// Used to retrieve a singleton asset from a value with a specific policy id
pub fn get_singleton_asset_with_policy(
  value: Value,
  policy_id: PolicyId,
) -> Pair<AssetName, Int> {
  expect [p] =
    value
      |> assets.tokens(policy_id) //return dict of policy id to asset name and quantity
      |> dict.to_pairs

  p
}

// Verify a 32-byte hash (Blake2b-256)
pub fn verify_hash_32(data: Data, data_hash: H32<Data>) {
  expect blake2b_256(cbor.serialise(data)) == data_hash
}

// Verify a 28-byte hash (Blake2b-224)
pub fn verify_hash_28(data: Data, data_hash: H28<Data>) {
  expect blake2b_224(cbor.serialise(data)) == data_hash
}

pub fn get_verification_key_hash(key: VerificationKey) -> VerificationKeyHash {
  blake2b_224(key)
}
