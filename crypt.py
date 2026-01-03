import string
from collections import Counter
from typing import Tuple, Dict, List

# Fréquences moyennes des lettres en français
FR_FREQUENCIES = {
    'e': 17.26, 'a': 8.23, 'i': 7.24, 'o': 5.28, 'n': 7.15, 's': 7.94,
    'r': 6.64, 't': 7.30, 'u': 6.05, 'l': 5.34, 'd': 3.67, 'c': 3.15,
    'p': 3.01, 'm': 2.74, 'h': 0.92, 'g': 1.04, 'f': 1.07, 'b': 1.47,
    'v': 1.13, 'q': 0.89, 'j': 0.89, 'k': 0.00, 'w': 0.00, 'x': 0.54,
    'y': 0.46, 'z': 0.12
}

# Mots français courants pour validation
FR_COMMON_WORDS = {
    'le', 'la', 'de', 'et', 'à', 'un', 'une', 'les', 'des',
    'en', 'par', 'pour', 'dans', 'avec', 'sur', 'que', 'qui',
    'est', 'il', 'elle', 'vous', 'nous', 'je', 'tu', 'ce',
    'au', 'du', 'se', 'pas', 'plus', 'bien', 'peu', 'fait'
}

class CryptoAnalyzer:
    def __init__(self, encrypted_text: str):
        self.encrypted = encrypted_text.lower()
        self.clean_text = ''.join(c for c in self.encrypted if c.isalpha())
    
    def caesar_decrypt(self, text: str, shift: int) -> str:
        """Déchiffre un texte avec un décalage César"""
        result = []
        for c in text:
            if c.isalpha():
                base = ord('a')
                shifted = (ord(c) - base - shift) % 26
                result.append(chr(base + shifted))
            else:
                result.append(c)
        return ''.join(result)
    
    def monoalpha_decrypt(self, text: str, key: Dict[str, str]) -> str:
        """Déchiffre avec une clé de substitution mono-alphabétique"""
        return ''.join(key.get(c, c) for c in text)
    
    def chi_squared_score(self, text: str) -> float:
        """Calcule le chi-squared entre le texte et les fréquences du français"""
        text_clean = ''.join(c for c in text if c.isalpha())
        
        if not text_clean:
            return float('inf')
        
        freq_count = Counter(text_clean)
        chi2 = 0
        
        for letter in string.ascii_lowercase:
            observed = freq_count.get(letter, 0)
            expected = (FR_FREQUENCIES.get(letter, 0) / 100) * len(text_clean)
            
            if expected > 0:
                chi2 += ((observed - expected) ** 2) / expected
        
        return chi2
    
    def word_score(self, text: str) -> float:
        """Évalue la présence de mots français courants"""
        words = text.lower().split()
        words_clean = [''.join(c for c in w if c.isalpha()) for w in words]
        
        if not words_clean:
            return 0
        
        matches = sum(1 for w in words_clean if w in FR_COMMON_WORDS and len(w) > 2)
        return matches / len(words_clean)
    
    def combined_score(self, text: str) -> float:
        """Combine chi-squared et score de mots (inférieur = mieux)"""
        chi2 = self.chi_squared_score(text)
        word_bonus = self.word_score(text) * 50
        
        return chi2 - word_bonus
    
    def break_caesar(self) -> Tuple[int, str, float]:
        """Teste tous les décalages César (0-25)"""
        results = []
        
        for shift in range(26):
            decrypted = self.caesar_decrypt(self.encrypted, shift)
            score = self.combined_score(decrypted)
            results.append((shift, decrypted, score))
        
        best = min(results, key=lambda x: x[2])
        return best
    
    def break_monoalpha_simple(self) -> Tuple[str, float]:
        """Analyse simple mono-alphabétique par analyse de fréquences"""
        text_freq = Counter(self.clean_text)
        sorted_encrypted = sorted(text_freq.items(), key=lambda x: x[1], reverse=True)
        
        sorted_french = sorted(
            FR_FREQUENCIES.items(), key=lambda x: x[1], reverse=True
        )
        
        key = {}
        for (enc_char, _), (fr_char, _) in zip(sorted_encrypted, sorted_french):
            key[enc_char] = fr_char
        
        decrypted = self.monoalpha_decrypt(self.encrypted, key)
        score = self.combined_score(decrypted)
        
        return decrypted, score


def analyze_text(encrypted_text: str, cipher_type: str = "auto"):
    """Analyse un texte chiffré et affiche les résultats"""
    
    analyzer = CryptoAnalyzer(encrypted_text)
    
    print("=" * 70)
    print("CRYPTANALYSE INTELLIGENTE AUTOMATIQUE")
    print("=" * 70)
    print(f"\nTexte chiffré : {encrypted_text[:60]}...")
    print(f"Longueur : {len(analyzer.clean_text)} caractères")
    
    if cipher_type.lower() in ["caesar", "auto"]:
        print("\n" + "-" * 70)
        print("ANALYSE CÉSAR (décalage simple)")
        print("-" * 70)
        
        shift, decrypted, score = analyzer.break_caesar()
        print(f"Clé trouvée : Décalage de {shift} positions")
        print(f"Score de confiance : {score:.2f} (inférieur = mieux)")
        print(f"\nTexte déchiffré :\n{decrypted[:100]}...\n")
        
        if len(decrypted) <= 200:
            print(f"Texte complet :\n{decrypted}\n")
    
    if cipher_type.lower() in ["monoalpha", "auto"]:
        print("-" * 70)
        print("ANALYSE MONO-ALPHABÉTIQUE (substitution simple)")
        print("-" * 70)
        
        decrypted, score = analyzer.break_monoalpha_simple()
        print(f"Analyse par fréquences appliquée")
        print(f"Score de confiance : {score:.2f}")
        print(f"\nTexte déchiffré :\n{decrypted[:100]}...\n")
        
        if len(decrypted) <= 200:
            print(f"Texte complet :\n{decrypted}\n")


# ============ UTILISATION PERSONNALISÉE ============
def usage_personnalisee():
    """
    Exemples d'utilisation pour analyser tes propres messages
    """
    print("\n" + "=" * 70)
    print("UTILISATION PERSONNALISÉE")
    print("=" * 70)
    
    # Exemple 1 : Texte chiffré personnalisé
    print("\n--- Exemple 1 : Ton propre texte chiffré ---\n")
    ton_texte_chiffre = "uryyb jbeyq"  # "hello world" en ROT13 (décalage 13)
    analyzer = CryptoAnalyzer(ton_texte_chiffre)
    shift, decrypted, score = analyzer.break_caesar()
    print(f"Texte chiffré : {ton_texte_chiffre}")
    print(f"Texte déchiffré : {decrypted}")
    print(f"Clé trouvée : Décalage {shift}")
    
    # Exemple 2 : Analyse mono-alphabétique
    print("\n--- Exemple 2 : Substitution personnalisée ---\n")
    ton_texte2 = "ur oxmmdvu cru kud rudrriau cru qdpvxiu"
    analyzer2 = CryptoAnalyzer(ton_texte2)
    decrypted2, score2 = analyzer2.break_monoalpha_simple()
    print(f"Texte chiffré : {ton_texte2}")
    print(f"Texte probable : {decrypted2}")
    
    # Exemple 3 : Créer ton propre chiffrement
    print("\n--- Exemple 3 : Chiffrer un message puis le décrypter ---\n")
    mon_secret = "ceci est un secret"
    analyzer3 = CryptoAnalyzer(mon_secret)
    
    # Chiffrer avec décalage 7
    encrypted = analyzer3.caesar_decrypt(mon_secret, -7)
    print(f"Message original : {mon_secret}")
    print(f"Message chiffré (décalage 7) : {encrypted}")
    
    # Décrypter automatiquement
    analyzer4 = CryptoAnalyzer(encrypted)
    shift4, decrypted4, score4 = analyzer4.break_caesar()
    print(f"Message décrypté : {decrypted4}")
    print(f"Clé retrouvée : {shift4}")


# ============ TESTS ============
if __name__ == "__main__":
    # Test 1 : Chiffre de César
    print("\n### TEST 1 : CHIFFRE DE CÉSAR ###\n")
    message1 = "Bonjour, ceci est un message secret avec un chiffre de César"
    encrypted1 = CryptoAnalyzer(message1).caesar_decrypt(message1, -3)
    analyze_text(encrypted1, "caesar")
    
    # Test 2 : Substitution mono-alphabétique simple
    print("\n\n### TEST 2 : SUBSTITUTION MONO-ALPHABÉTIQUE ###\n")
    message2 = "le chiffre de substitution est une methode ancienne"
    key = str.maketrans(
        "abcdefghijklmnopqrstuvwxyz",
        "qwertyuiopasdfghjklzxcvbnm"
    )
    encrypted2 = message2.translate(key)
    analyze_text(encrypted2, "monoalpha")
    
    # Test 3 : Mode automatique
    print("\n\n### TEST 3 : MODE AUTOMATIQUE ###\n")
    message3 = "cryptanalyse automatique"
    analyzer3 = CryptoAnalyzer(message3)
    encrypted3 = analyzer3.caesar_decrypt(message3, -5)
    analyze_text(encrypted3, "auto")
    
    # Lancer l'utilisation personnalisée
    usage_personnalisee()