


#Começa na lateral 4
lateral = 4;
#Cor da lavanderia que o robô chegou
corLav = coresLavanderias[0][0];

#Caso a cor do bloco seja a mesma da lavanderia que o robô chegou, dá pra pegar o bloco.
#Caso não, como não teremos verificado as outras linhas descendo, não sabemos se terá bloco ao lado.

enquanto(!lavanderiaOposta()){
  distLavOposta = 0;
  descerLateral();
   giraParaEsquerda();
   if(verificaLinha()){
       buscarBloco();
   }else{
       giraParaDireita();
       descerLateral();
   }
}
 descerLateral(){
  "mover até o meio do quadrado";
  }

  giraParaEsquerda(){
  "gira 90º"
   verificaLinha();
  }

  verificaLinha(){
    if (ultrassom.value < "tamanho até a parede aposta"){
        return True;
      }else{
          return False;
                }
  }

buscarBloco(){
   coluna = 0;
   enquanto(!pegouOBloco()){
       if(naProximaCasaEstaOBloco()){
           if (verficaBloco())
                pegaOBloco();
              else {
                largaBloco();
              }
       }else{
           coluna +=coluna;
           andarColuna();
       }
   }
   cor = verificarCorBloco();
   if(corInicio != cor){
       largaBloco();
   }else{
       voltarQuantidadeColunas();
       giraParaEsquerda();
       voltarQuantidadeLinhas();
       largaBloco();
       addMatrizAondeColocouBloco();
   }
}