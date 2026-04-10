// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title BurgessClaimsRegistry
 * @notice Lightweight on-chain registry for Burgess Claims — immutable,
 *         auditable commitment fingerprints that prove a human demanded
 *         oversight at a specific point in time.
 *
 * @dev Stores only minimal data: commitment hash, signature, target,
 *      category, and block timestamp. Full claim details remain encrypted
 *      in the claimant's local Sovereign Personal Vault.
 *
 *      Signature verification (Ed25519) is performed off-chain — the
 *      contract stores the signature bytes for public auditability but
 *      does not verify them on-chain (EVM does not natively support
 *      Ed25519).
 */
contract BurgessClaimsRegistry {
    // ---------------------------------------------------------------
    // Types
    // ---------------------------------------------------------------

    struct Claim {
        bytes32 commitmentHash;
        bytes signature;
        address issuer;
        string target;
        string category;
        uint256 expiry;
        uint256 blockTimestamp;
    }

    struct Response {
        bytes32 responseCommitment;
        bytes responderSignature;
        address responder;
        uint256 responseTimestamp;
    }

    // ---------------------------------------------------------------
    // State
    // ---------------------------------------------------------------

    Claim[] private claims;
    mapping(uint256 => Response) private responses;

    // ---------------------------------------------------------------
    // Events
    // ---------------------------------------------------------------

    event ClaimIssued(
        uint256 indexed claimId,
        bytes32 commitmentHash,
        address indexed issuer,
        string target,
        string category
    );

    event ClaimResponse(
        uint256 indexed claimId,
        bytes32 responseCommitment,
        address indexed responder
    );

    // ---------------------------------------------------------------
    // Write functions
    // ---------------------------------------------------------------

    /**
     * @notice Issue a new Burgess Claim by posting its commitment
     *         fingerprint on-chain.
     * @param commitmentHash SHA-256 hash of the off-chain claim data.
     * @param signature      Ed25519 signature over the commitment hash.
     * @param target         Identifier of the institution / system addressed.
     * @param category       Claim category (e.g. "enforcement", "dispute").
     * @param expiry         Optional expiry timestamp (0 = no expiry).
     * @return claimId       The sequential ID assigned to this claim.
     */
    function issueClaim(
        bytes32 commitmentHash,
        bytes calldata signature,
        string calldata target,
        string calldata category,
        uint256 expiry
    ) external returns (uint256 claimId) {
        require(commitmentHash != bytes32(0), "Empty commitment hash");
        require(signature.length > 0, "Empty signature");
        require(bytes(target).length > 0, "Empty target");
        require(bytes(category).length > 0, "Empty category");
        require(
            expiry == 0 || expiry > block.timestamp,
            "Expiry must be in the future or zero"
        );

        claimId = claims.length;

        claims.push(
            Claim({
                commitmentHash: commitmentHash,
                signature: signature,
                issuer: msg.sender,
                target: target,
                category: category,
                expiry: expiry,
                blockTimestamp: block.timestamp
            })
        );

        emit ClaimIssued(claimId, commitmentHash, msg.sender, target, category);
    }

    /**
     * @notice Submit a response to an existing claim.
     * @param claimId             ID of the claim being responded to.
     * @param responseCommitment  SHA-256 hash of the response details.
     * @param responderSignature  Signature from the responding party.
     */
    function respondToClaim(
        uint256 claimId,
        bytes32 responseCommitment,
        bytes calldata responderSignature
    ) external {
        require(claimId < claims.length, "Claim does not exist");
        require(responseCommitment != bytes32(0), "Empty response commitment");
        require(responderSignature.length > 0, "Empty responder signature");
        require(
            responses[claimId].responder == address(0),
            "Claim already has a response"
        );

        responses[claimId] = Response({
            responseCommitment: responseCommitment,
            responderSignature: responderSignature,
            responder: msg.sender,
            responseTimestamp: block.timestamp
        });

        emit ClaimResponse(claimId, responseCommitment, msg.sender);
    }

    // ---------------------------------------------------------------
    // Read functions
    // ---------------------------------------------------------------

    /**
     * @notice Retrieve a claim by its ID.
     */
    function getClaim(uint256 claimId)
        external
        view
        returns (
            bytes32 commitmentHash,
            bytes memory signature,
            address issuer,
            string memory target,
            string memory category,
            uint256 expiry,
            uint256 blockTimestamp
        )
    {
        require(claimId < claims.length, "Claim does not exist");
        Claim storage c = claims[claimId];
        return (
            c.commitmentHash,
            c.signature,
            c.issuer,
            c.target,
            c.category,
            c.expiry,
            c.blockTimestamp
        );
    }

    /**
     * @notice Return the total number of claims issued.
     */
    function getClaimCount() external view returns (uint256) {
        return claims.length;
    }

    /**
     * @notice Retrieve the response to a claim, if one exists.
     */
    function getResponse(uint256 claimId)
        external
        view
        returns (
            bytes32 responseCommitment,
            bytes memory responderSignature,
            address responder,
            uint256 responseTimestamp
        )
    {
        require(claimId < claims.length, "Claim does not exist");
        Response storage r = responses[claimId];
        return (
            r.responseCommitment,
            r.responderSignature,
            r.responder,
            r.responseTimestamp
        );
    }
}
