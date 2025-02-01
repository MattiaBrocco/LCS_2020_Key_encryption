# LCS_2020_Key_encryption

## 🔑 Optimized Brute Force Attack with Gradient Descent
This project implements an optimized brute force attack for **cipher decryption**, replacing exhaustive key search with a gradient-based hill climbing approach. Instead of testing all possible keys, the algorithm intelligently mutates and refines keys iteratively to maximize plaintext likelihood, significantly improving efficiency.

## 🚀 Features
* Gradient-based key search instead of brute-force iteration
* Adaptive key mutation for faster convergence
* Automatic hash verification to detect the correct key
* Flexible optimization with customizable iterations

## 🔧 Usage
This function refines an initial key guess (`key0`) using a gradient-like approach:

```python
best_key = gradient_descent_brute_force(key0, text, corpus, correct_hash, ciphertext)
```
It iteratively modifies the key, evaluating improvements based on corpus scoring, and stops when the correct decryption hash is found.

## 📜 How It Works
1. Start with an initial key guess (from frequency analysis).
2. Mutate the key slightly (e.g., swap letters in substitution ciphers).
3. Evaluate plaintext quality using a scoring function.
4. Iterate until an improved key is found or the correct hash is matched.
5. This method greatly reduces computational cost while maintaining decryption accuracy.

## 🛠 Future Enhancements
* Implement Simulated Annealing to escape local optima.
* Extend to Genetic Algorithms for broader key search.