function recherche(){
    let recherche_film = document.getElementById("Recherche").value.trim().toLowerCase();// tolowercase cela met toute en minuscule et trim enleve les espace
    
    // Récupérer tous les divs contenant les films (liste)
    let films = document.querySelectorAll('.image_rangement > div'); // je creer une liste avec toute les div qu'il y a dans la div avec la classe image_rangement
    
    films.forEach(film => { // Pour chaque div je fait tel action
        let titre = film.querySelector('figcaption').textContent.toLowerCase();// Récupérer le texte du figcaption (titre du film)
        // Afficher ou masquer selon si le titre commence par la recherche
        if(recherche_film === "" || titre.startsWith(recherche_film)){ // les 2 bares parallele veut dire "OU"
            film.style.display = "block";//on decide de laisser afficher la div car soit la liste est vide donc on affiche tout soit on afiche car elle commence par ce qu'il y a dans la recherche
        } else {
            film.style.display = "none";// on decide de cacher la div du film
        }
    });
}
function etoiles1(){
    let etoile1 = document.getElementById("etoile1");
    etoile1.src = "../Image/etoile_pleine.png";
    let etoile2 = document.getElementById("etoile2");
    etoile2.src = "../Image/etoile_vide.png";
    let etoile3 = document.getElementById("etoile3");
    etoile3.src = "../Image/etoile_vide.png";
    let etoile4 = document.getElementById("etoile4");
    etoile4.src = "../Image/etoile_vide.png";
    let etoile5 = document.getElementById("etoile5");
    etoile5.src = "../Image/etoile_vide.png";
}

function etoiles2(){
    let etoile1 = document.getElementById("etoile1");
    etoile1.src = "../Image/etoile_pleine.png";
    let etoile2 = document.getElementById("etoile2");
    etoile2.src = "../Image/etoile_pleine.png";
    let etoile3 = document.getElementById("etoile3");
    etoile3.src = "../Image/etoile_vide.png";
    let etoile4 = document.getElementById("etoile4");
    etoile4.src = "../Image/etoile_vide.png";
    let etoile5 = document.getElementById("etoile5");
    etoile5.src = "../Image/etoile_vide.png";
}

function etoiles3(){
    let etoile1 = document.getElementById("etoile1");
    etoile1.src = "../Image/etoile_pleine.png";
    let etoile2 = document.getElementById("etoile2");
    etoile2.src = "../Image/etoile_pleine.png";
    let etoile3 = document.getElementById("etoile3");
    etoile3.src = "../Image/etoile_pleine.png";
    let etoile4 = document.getElementById("etoile4");
    etoile4.src = "../Image/etoile_vide.png";
    let etoile5 = document.getElementById("etoile5");
    etoile5.src = "../Image/etoile_vide.png";
}

function etoiles4(){
    let etoile1 = document.getElementById("etoile1");
    etoile1.src = "../Image/etoile_pleine.png";
    let etoile2 = document.getElementById("etoile2");
    etoile2.src = "../Image/etoile_pleine.png";
    let etoile3 = document.getElementById("etoile3");
    etoile3.src = "../Image/etoile_pleine.png";
    let etoile4 = document.getElementById("etoile4");
    etoile4.src = "../Image/etoile_pleine.png";
    let etoile5 = document.getElementById("etoile5");
    etoile5.src = "../Image/etoile_vide.png";
}

function etoiles5(){
    let etoile1 = document.getElementById("etoile1");
    etoile1.src = "../Image/etoile_pleine.png";
    let etoile2 = document.getElementById("etoile2");
    etoile2.src = "../Image/etoile_pleine.png";
    let etoile3 = document.getElementById("etoile3");
    etoile3.src = "../Image/etoile_pleine.png";
    let etoile4 = document.getElementById("etoile4");
    etoile4.src = "../Image/etoile_pleine.png";
    let etoile5 = document.getElementById("etoile5");
    etoile5.src = "../Image/etoile_pleine.png";
}