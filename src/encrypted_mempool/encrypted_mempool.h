// Copyright (c) 2025, The RSDT Project
// 
// All rights reserved.

#ifndef ENCRYPTED_MEMPOOL_H
#define ENCRYPTED_MEMPOOL_H

#include <vector>
#include <memory>
#include <crypto/crypto.h>
#include <cryptonote_basic/cryptonote_basic.h>

namespace encrypted_mempool {

// Encrypted transaction wrapper
struct EncryptedTx {
    crypto::public_key peer_key;
    std::vector<uint8_t> encrypted_data;
    crypto::hash8 nonce;
    uint64_t timestamp;
    
    EncryptedTx() = default;
    EncryptedTx(const crypto::public_key& key, const std::vector<uint8_t>& data, const crypto::hash8& n, uint64_t ts);
};

// Mempool encryption manager
class EncryptedMempool {
public:
    EncryptedMempool();
    ~EncryptedMempool();
    
    // Initialize encryption system
    bool init();
    
    // Check if encryption is enabled
    bool is_enabled() const { return m_enabled; }
    
    // Set encryption mode (opportunistic vs mandatory)
    void set_mode(bool opportunistic) { m_opportunistic = opportunistic; }
    
    // Encrypt transaction for peer
    bool encrypt_transaction(const cryptonote::transaction& tx, const crypto::public_key& peer_key, EncryptedTx& encrypted_tx);
    
    // Decrypt transaction from peer
    bool decrypt_transaction(const EncryptedTx& encrypted_tx, cryptonote::transaction& tx);
    
    // Generate ephemeral key pair for peer connection
    bool generate_peer_keys(crypto::public_key& pub_key, crypto::secret_key& sec_key);
    
    // Store peer's public key
    void add_peer(const crypto::public_key& peer_key);
    
    // Remove peer
    void remove_peer(const crypto::public_key& peer_key);
    
    // Check if peer supports encryption
    bool peer_supports_encryption(const crypto::public_key& peer_key) const;
    
private:
    bool m_enabled;
    bool m_opportunistic;
    std::map<crypto::public_key, crypto::secret_key> m_peer_keys;
    crypto::secret_key m_local_secret_key;
    crypto::public_key m_local_public_key;
    
    // Generate shared secret with peer
    bool generate_shared_secret(const crypto::public_key& peer_key, crypto::secret_key& shared_secret);
    
    // Encrypt data with shared secret
    bool encrypt_data(const std::vector<uint8_t>& data, const crypto::secret_key& key, std::vector<uint8_t>& encrypted);
    
    // Decrypt data with shared secret
    bool decrypt_data(const std::vector<uint8_t>& encrypted, const crypto::secret_key& key, std::vector<uint8_t>& data);
};

// Global encrypted mempool instance
extern std::unique_ptr<EncryptedMempool> g_encrypted_mempool;

// Initialize encrypted mempool system
bool init_encrypted_mempool(bool enabled = true, bool opportunistic = true);

// Check if encrypted mempool is enabled
bool is_encrypted_mempool_enabled();

// Encrypt transaction for broadcasting
bool encrypt_transaction_for_broadcast(const cryptonote::transaction& tx, const crypto::public_key& peer_key, EncryptedTx& encrypted_tx);

// Decrypt received transaction
bool decrypt_received_transaction(const EncryptedTx& encrypted_tx, cryptonote::transaction& tx);

} // namespace encrypted_mempool

#endif // ENCRYPTED_MEMPOOL_H

