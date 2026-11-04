from loja import calcular_desconto

def test_compra_acima_de_100_sem_fidelidade():
    assert calcular_desconto(200.0, fidelidade=False) == 180.0

def test_compra_abaixo_de_100_com_fidelidade():
    assert calcular_desconto(50.0, fidelidade=True) == 47.5

# --- Novos testes para matar os mutantes ---
def test_valor_exato_de_borda_100():
    # Exatamente 100.0 NÃO deve receber 10% de desconto
    assert calcular_desconto(100.0, fidelidade=False) == 100.0

def test_compra_acima_de_100_com_fidelidade():
    # 200 - 15% (10% + 5%) = 170.0
    assert calcular_desconto(200.0, fidelidade=True) == 170.0
