from encryption import generate_key, encrypt_message, decrypt_message

# Gera uma nova chave
# generate_key()

# Testa a criptografia e a descriptografia
def test_encryption():
    original_message = "Esta é uma mensagem secreta!"
    print(f"Mensagem original: {original_message}")

    # Criptografa a mensagem
    encrypted_message = encrypt_message(original_message)
    print(f"Mensagem criptografada: {encrypted_message}")

    # Descriptografa a mensagem
    decrypted_message = decrypt_message(encrypted_message)
    print(f"Mensagem descriptografada: {decrypted_message}")

    # Verifica se a mensagem original é igual à mensagem descriptografada
    assert original_message == decrypted_message, "Erro: A mensagem descriptografada não coincide com a original!"
    print("Teste de criptografia e descriptografia bem-sucedido!")

if __name__ == "__main__":
    test_encryption()
