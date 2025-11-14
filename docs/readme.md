# Sistema RPA de Extração e Processamento de Balancetes – Postalis

## 1. Visão Geral

Este projeto tem como objetivo automatizar o processo de **extração, processamento e validação de informações contábeis** relacionadas aos balancetes do sistema **Atena**. O sistema RPA (Robotic Process Automation) desenvolvido permite:

- Extrair balancetes do sistema contábil do Atena.
- Importar arquivos em PDF e Excel.
- Processar e transformar os dados em planilhas padronizadas.
- Validar movimentações de conciliação contábil das folhas de benefícios.

O sistema foi desenvolvido em **Python**, utilizando **Tkinter** para a interface gráfica, **Selenium** para automação web e bibliotecas auxiliares para manipulação de arquivos e planilhas.

---

## 2. Funcionalidades

1. **Extração de Balancetes**
   - Login automático no sistema Atena.
   - Seleção de planos específicos.
   - Download e armazenamento dos balancetes em pasta definida pelo usuário.

2. **Importação de Arquivos**
   - Leitura de arquivos PDF e Excel.
   - Extração de dados relevantes para conciliação contábil.

3. **Processamento e Transformação**
   - Conversão de dados em planilhas organizadas.
   - Atualização automática das abas de análise financeira.
   - Consolidação de informações de diferentes fontes (balancetes, remanejamentos, previsão orçamentária).

4. **Validação Contábil**
   - Conferência de movimentações e conciliações de folhas de benefícios.
   - Relatórios de divergências para auditoria e revisão.

---

## 3. Estrutura do Projeto