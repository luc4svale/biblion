"""Add initial seed data

Revision ID: 7941c1ce33c6
Revises: a4478f945f1f
Create Date: 2025-03-05 21:18:57.566353

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from datetime import datetime, timezone


# revision identifiers, used by Alembic.
revision = '7941c1ce33c6'
down_revision = 'a4478f945f1f'
branch_labels = None
depends_on = None


def upgrade():
    # Criando referência às tabelas existentes
    categories_table = table('categories',
        column('id', sa.String(36)),
        column('name', sa.String(100)),
        column('created_at', sa.DateTime),
        column('updated_at', sa.DateTime)
    )

    authors_table = table('authors',
        column('id', sa.String(36)),
        column('name', sa.String(150)),
        column('created_at', sa.DateTime),
        column('updated_at', sa.DateTime)
    )

    publishers_table = table('publishers',
        column('id', sa.String(36)),
        column('name', sa.String(150)),
        column('created_at', sa.DateTime),
        column('updated_at', sa.DateTime)
    )

    books_table = table('books',
        column('id', sa.String(36)),
        column('title', sa.String(200)),
        column('synopsis', sa.Text),
        column('publication_year', sa.Integer),
        column('file', sa.String(70)),
        column('cover', sa.String(70)),
        column('author_id', sa.String(36)),
        column('category_id', sa.String(36)),
        column('publisher_id', sa.String(36)),
        column('created_at', sa.DateTime),
        column('updated_at', sa.DateTime)
    )
    
    
    favorites_table = table('favorites',
        column('id', sa.String(36)),
        column('user_id', sa.String(36)),
        column('book_id', sa.String(36)),
        column('created_at', sa.DateTime)
    )

    

    op.bulk_insert(categories_table, [
        {"id": "ffa55698-7fe3-4349-bfb4-a8cd36df7637", "name": "Romance", "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)},
        {"id": "9a3c520b-3488-4978-a8e3-745d1c837191", "name": "Fantasia", "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)},
        {"id": "635f0169-8c7e-4a4e-878d-7493eaf3ede8", "name": "Ficção Científica", "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)},
        {"id": "ad49d025-0c5b-4da8-926a-70abcf954558", "name": "Drama", "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)},
    ])


    op.bulk_insert(authors_table, [
        {"id": "813cc342-2d70-4038-9ef0-a6bfca059cb2", "name": "Cecelia Ahern", "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)},
        {"id": "e8618c4e-1e89-41a8-87bc-c59f1a14b5fe", "name": "C. C. Hunter", "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)},
        {"id": "c60c1af8-c092-4a64-bfc2-b3012ba19a32", "name": "Colleen Hoover", "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)},
        {"id": "0cc74a76-6e10-40aa-9eb3-40606ee09750", "name": "Beth O'Leary", "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)},
        {"id": "5a2007a2-d5fd-409d-83cb-eef2a3db213c", "name": "Leigh Bardugo", "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)},
        {"id": "da4c14da-80b2-4986-9466-4373e5a7a01c", "name": "Rick Riordan", "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)},
        {"id": "5e81f437-f21e-4c25-8af3-a9586d8bea88", "name": "Victoria Aveyard", "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)},
        {"id": "4187a934-b4e3-4bae-97ef-878692b46cec", "name": "J.R.R. Tolkien", "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)},
        {"id": "811e8ccf-0c1f-44ad-932d-32de1a2f7312", "name": "Frank Herbert", "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)},
    ])
    
    
    op.bulk_insert(publishers_table, [
        {"id": "0c776435-3235-405c-b8ac-3a28dbab9ef0", "name": "Novo Conceito", "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)},
        {"id": "8e7e4416-25b0-4734-935c-b9d9bcc95219", "name": "Jangada", "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)},
        {"id": "0378898c-fc08-40ad-87ba-800d86768e66", "name": "Galera", "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)},
        {"id": "49ed4222-6eac-4e24-a865-7cfcee249ede", "name": "Intrínseca", "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)},
        {"id": "c5a09d3b-5327-4126-b50c-2bbc93129df0", "name": "Planeta Minotauro", "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)},
        {"id": "c30ba950-deac-4572-ae54-b26bb66f0900", "name": "Seguinte", "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)},
        {"id": "aae2d6aa-031b-4291-98ec-b92536a401b5", "name": "HarperCollins", "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)},
        {"id": "df7e8152-ac23-48c7-ac25-ef37766fbcac", "name": "Aleph", "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)},
    ])
    
    
    
        # Inserindo livros iniciais
    op.bulk_insert(books_table, [
        {
         "id": "49e383be-a685-4c1a-8344-2f47d214dfca", 
         "title": "P.S. Eu Te Amo", 
         "synopsis": "Gerry e Holly eram namorados de infância e ficariam juntos para sempre, até que o inimaginável acontece e Gerry morre, deixando-a devastada. Conforme seu aniversário de 30 anos se aproxima, Holly descobre um pacote de cartas nas quais Gerry, gentilmente, a guia em sua nova vida sem ele. Com ajuda de seus amigos e de sua família barulhenta e carinhosa, Holly consegue rir, chorar, cantar, dançar e ser mais corajosa do que nunca.",
         "publication_year": 2012, 
         "author_id": "813cc342-2d70-4038-9ef0-a6bfca059cb2", 
         "category_id": "ffa55698-7fe3-4349-bfb4-a8cd36df7637",
         "publisher_id": "0c776435-3235-405c-b8ac-3a28dbab9ef0", 
         "created_at": datetime.now(timezone.utc),
         "updated_at": datetime.now(timezone.utc),
         "file": "2738c5d8b640c4ae76dfb41587fe44ae.pdf", 
         "cover": "398edb95c98dc9d19c1a8e7da124bd7d4f3a3dde5a1ede3eada2f7e1c16b9d27.jpeg",
        },
        
        {
         "id": "401be96c-48f2-4af6-83e2-54cb8dddd7c4", 
         "title": "Eu e esse meu coração", 
         "synopsis": "Quando Liz e Matt se conhecem, suas vidas já estavam entrelaçadas de uma forma inesperada. Liz nasceu com um problema cardíaco e sobreviveu graças a um transplante. Matt perdeu a irmã no mesmo dia em que Liz recebeu um novo coração. Anos depois, o destino os aproxima, despertando sentimentos e segredos que podem mudar tudo. Entre memórias, dúvidas e o peso do passado, ambos precisarão decidir se vale a pena seguir em frente juntos. Uma história emocionante sobre amor, perda e recomeços.",
         "publication_year": 2018, 
         "author_id": "e8618c4e-1e89-41a8-87bc-c59f1a14b5fe", 
         "category_id": "ffa55698-7fe3-4349-bfb4-a8cd36df7637",
         "publisher_id": "8e7e4416-25b0-4734-935c-b9d9bcc95219", 
         "created_at": datetime.now(timezone.utc),
         "updated_at": datetime.now(timezone.utc),
         "file": "5591a9f6d4c479a14708154ba0f01f78.pdf", 
         "cover": "a4f0e45708cda3f7eaca6f0b0554535e6f31d88f9d57b88c62485e14a621ffef.jpeg",
        },
        {
         "id": "75bbfe89-f898-4ae0-a66d-5e4acba8da2f", 
         "title": "É assim que acaba", 
         "synopsis": "Lily Bloom sempre acreditou no amor, apesar de seu passado difícil. Ao conhecer Ryle Kincaid, um neurocirurgião encantador, tudo parece perfeito, mas logo ela percebe que nem tudo é o que parece. Quando seu primeiro amor, Atlas Corrigan, reaparece, segredos do passado vêm à tona, forçando Lily a confrontar verdades dolorosas. Entre paixão e dor, ela precisa tomar a decisão mais difícil de sua vida. Uma história intensa sobre amor, superação e a coragem de recomeçar.",
         "publication_year": 2018, 
         "author_id": "c60c1af8-c092-4a64-bfc2-b3012ba19a32", 
         "category_id": "ffa55698-7fe3-4349-bfb4-a8cd36df7637",
         "publisher_id": "0378898c-fc08-40ad-87ba-800d86768e66", 
         "created_at": datetime.now(timezone.utc),
         "updated_at": datetime.now(timezone.utc),
         "file": "ab93c4408f0354f39fb556407d0962cd.pdf", 
         "cover": "3aa612eeb660f6801a2f393910545e39b563496559781f0c76c3caad534074f6.jpeg",
        },
        {
         "id": "06914800-74b5-4343-8d23-474782c399dd", 
         "title": "Teto para dois", 
         "synopsis": "Tiffy e Leon precisam dividir um apartamento, mas nunca se encontram. Ela ocupa o espaço à noite, enquanto ele trabalha no turno da madrugada. Comunicando-se apenas por bilhetes colados pela casa, eles compartilham segredos, medos e momentos divertidos. O que começa como um acordo inusitado se transforma em uma conexão inesperada. Quando seus mundos colidem de verdade, terão que decidir se um relacionamento pode surgir dessa convivência peculiar. Uma comédia romântica leve e envolvente sobre amor e amizade.",
         "publication_year": 2019, 
         "author_id": "0cc74a76-6e10-40aa-9eb3-40606ee09750", 
         "category_id": "ffa55698-7fe3-4349-bfb4-a8cd36df7637",
         "publisher_id": "49ed4222-6eac-4e24-a865-7cfcee249ede", 
         "created_at": datetime.now(timezone.utc),
         "updated_at": datetime.now(timezone.utc),
         "file": "88db1d5c06fb65f05ab984045ab39011.pdf", 
         "cover": "3e6026e67a8efc392b3063c23126ba887c3c2bde70b3ca07005d5ba270ea7c5d.jpeg",
        },
        {
         "id": "1c36d5f6-f9f5-4d25-a5f8-090469262c3a", 
         "title": "Verity", 
         "synopsis": "Lowen Ashleigh, uma escritora em dificuldades, recebe a chance de terminar a série best-seller de Verity Crawford, uma autora famosa que está incapacitada. Ao se mudar para a casa de Verity, Lowen encontra uma autobiografia oculta, revelando segredos perturbadores sobre a autora e sua família. À medida que se envolve com Jeremy, marido de Verity, Lowen percebe que o perigo pode estar mais perto do que imagina. Um thriller psicológico intenso e cheio de reviravoltas, onde nada é o que parece.",
         "publication_year": 2020, 
         "author_id": "c60c1af8-c092-4a64-bfc2-b3012ba19a32", 
         "category_id": "ffa55698-7fe3-4349-bfb4-a8cd36df7637",
         "publisher_id": "0378898c-fc08-40ad-87ba-800d86768e66", 
         "created_at": datetime.now(timezone.utc),
         "updated_at": datetime.now(timezone.utc),
         "file": "32edf2186dbf89084124f78dda22bc66.pdf", 
         "cover": "ef310ecc4a91a4ad2436c52bb928e5c5a616859cd0d5656db86cae18260f31b8.jpeg",
        },
        {
         "id": "613af8de-6ee3-49bb-905d-84bac9ad80b4", 
         "title": "Sombra e Ossos", 
         "synopsis": "Alina Starkov é uma órfã e cartógrafa do exército que descobre ter um poder extraordinário capaz de mudar o destino de seu reino, Ravka. Ao ser levada para treinar com os Grishas, uma elite mágica liderada pelo misterioso e poderoso Darkling, Alina precisa aprender a controlar sua habilidade para destruir a Dobra das Sombras, uma força maligna que ameaça o mundo. Mas em meio a traições e segredos, ela descobre que o verdadeiro perigo pode estar mais perto do que imagina. Uma jornada épica de magia, guerra e autodescoberta.",
         "publication_year": 2021, 
         "author_id": "5a2007a2-d5fd-409d-83cb-eef2a3db213c", 
         "category_id": "9a3c520b-3488-4978-a8e3-745d1c837191",
         "publisher_id": "c5a09d3b-5327-4126-b50c-2bbc93129df0", 
         "created_at": datetime.now(timezone.utc),
         "updated_at": datetime.now(timezone.utc),
         "file": "c69cc9f0eaa9e0d4a5289a885c717c99.pdf", 
         "cover": "9f14c598329a196e5a9c0bb4ae91a15b73d1ceca1e6bbd5d6c70ba46fe10efb1.jpeg",
        },
        
        {
         "id": "15fc1069-3f4f-4baa-b197-f7cd47fb9b36", 
         "title": "O ladrão de raios", 
         "synopsis": "Percy Jackson descobre que é um semideus, filho de Poseidon, e que seu destino está ligado ao Olimpo. Acusado de roubar o raio-mestre de Zeus, ele tem apenas dez dias para recuperar o artefato e evitar uma guerra entre os deuses. Ao lado de seus amigos, Annabeth e Grover, Percy embarca em uma jornada repleta de desafios, criaturas mitológicas e segredos sobre sua própria origem. Enquanto luta para provar sua inocência, ele aprende que ser um herói significa muito mais do que ter poderes.",
         "publication_year": 2023, 
         "author_id": "da4c14da-80b2-4986-9466-4373e5a7a01c", 
         "category_id": "9a3c520b-3488-4978-a8e3-745d1c837191",
         "publisher_id": "49ed4222-6eac-4e24-a865-7cfcee249ede", 
         "created_at": datetime.now(timezone.utc),
         "updated_at": datetime.now(timezone.utc),
         "file": "97c354c78ff07603fe23cbadf426a978.pdf", 
         "cover": "2ffc899e3293b7d750489fd7accfd1c84caa31fb9d83a291b7a70ee04533b052.jpeg",
        },
        
        {
         "id": "c99a9ebc-d17a-4bb2-bc8a-d4bc7e20792f", 
         "title": "A rainha vermelha", 
         "synopsis": "Mare Barrow vive em um mundo dividido pelo sangue os Vermelhos, plebeus comuns, e os Prateados, elite com poderes sobre-humanos. Quando descobre que possui habilidades especiais, mesmo sendo Vermelha, Mare é forçada a viver entre os Prateados, fingindo ser uma nobre. Em meio a traições, intrigas e uma revolução iminente, ela precisa decidir em quem confiar. Enquanto luta por liberdade, descobre que no jogo pelo poder, ninguém é realmente quem parece ser. Uma história de fantasia cheia de ação e reviravoltas.",
         "publication_year": 2015, 
         "author_id": "5e81f437-f21e-4c25-8af3-a9586d8bea88", 
         "category_id": "9a3c520b-3488-4978-a8e3-745d1c837191",
         "publisher_id": "c30ba950-deac-4572-ae54-b26bb66f0900", 
         "created_at": datetime.now(timezone.utc),
         "updated_at": datetime.now(timezone.utc),
         "file": "be9278bb896bc609a2efa8f5773d83fa.pdf", 
         "cover": "e8bfcb24b96727c750352bf5d0dba4d45fb305efb66d6e63ceee9b350933c2c1.jpeg",
        },
        
        {
         "id": "99a3819f-011f-4a21-af51-b12e79fe866f", 
         "title": "O Hobbit", 
         "synopsis": "Bilbo Bolseiro leva uma vida tranquila até que o mago Gandalf e um grupo de treze anões o recrutam para uma grande aventura recuperar o tesouro guardado pelo dragão Smaug. Durante a jornada, Bilbo enfrenta trolls, goblins e criaturas perigosas, além de encontrar um anel misterioso que mudará seu destino. No caminho, ele descobre sua coragem e esperteza, provando que até o menor dos heróis pode fazer a diferença. Uma clássica história de fantasia repleta de magia, desafios e amizade.",
         "publication_year": 2019, 
         "author_id": "4187a934-b4e3-4bae-97ef-878692b46cec", 
         "category_id": "9a3c520b-3488-4978-a8e3-745d1c837191",
         "publisher_id": "aae2d6aa-031b-4291-98ec-b92536a401b5", 
         "created_at": datetime.now(timezone.utc),
         "updated_at": datetime.now(timezone.utc),
         "file": "aa12f955ab10c1e60906ee57c15ad6fc.pdf", 
         "cover": "06c0279094cda417fc3c88e7b45029cfb902f5122c57e28374da07ae68981ef3.jpeg",
        },
        
        
        {
         "id": "7b716d10-b718-46d9-8464-fc4fb3bde031", 
         "title": "Duna", 
         "synopsis": "No deserto de Arrakis, Paul Atreides é herdeiro de uma dinastia envolvida em uma guerra pelo controle da especiaria Melange, a mais valiosa do universo. Após uma traição, Paul foge e se une aos Fremen, aprendendo seus segredos e descobrindo um destino profético. Enquanto luta pela sobrevivência, ele precisa escolher entre vingança e liderança. Em um mundo de conspirações, profecias e batalhas épicas, Duna é uma jornada de poder, sacrifício e o preço de mudar o futuro.",
         "publication_year": 2017, 
         "author_id": "0cc74a76-6e10-40aa-9eb3-40606ee09750", 
         "category_id": "9a3c520b-3488-4978-a8e3-745d1c837191",
         "publisher_id": "df7e8152-ac23-48c7-ac25-ef37766fbcac", 
         "created_at": datetime.now(timezone.utc),
         "updated_at": datetime.now(timezone.utc),
         "file": "6f08bb168236dc53d99cfb36a36312b1.pdf", 
         "cover": "ed906d5c756b399d2fa34d6d4b0f078f08093e1a82c7e5e8a48c489548dc803a.jpeg",
        },
    ])
    
    
    op.bulk_insert(favorites_table, [
        {"id": "d4abda1b-35b2-46e0-8359-d37b547e506c", "user_id": "188bfdca-c0f5-4424-a12c-ec4c5de8c9e3", "book_id": "49e383be-a685-4c1a-8344-2f47d214dfca", "created_at": datetime.now(timezone.utc)},
        {"id": "54c2c068-563e-4c43-aefb-4dc6d4664ad4", "user_id": "188bfdca-c0f5-4424-a12c-ec4c5de8c9e3", "book_id": "75bbfe89-f898-4ae0-a66d-5e4acba8da2f", "created_at": datetime.now(timezone.utc)},
    ])

   
def downgrade():
    op.execute("DELETE FROM categories")
    op.execute("DELETE FROM authors")
    op.execute("DELETE FROM publishers")
    op.execute("DELETE FROM books")
    op.execute("DELETE FROM favorites")