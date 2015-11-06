# -*- coding: utf-8 -*-
from __future__ import absolute_import

import unittest

import constants
from models import Quotation
from quotations import QuotationValidator


class TestQuotationMap(unittest.TestCase):

    def test_pairing(self):
        """ Test to check that there is a closing quotation for every opening quotation """
        from utils import QUOTATION_MAP

        for quotations in QUOTATION_MAP.values():
            self.assertTrue(len(quotations) and len(quotations) % 2 == 0)


class TestQuotation(unittest.TestCase):

    def test_init_not_found(self):
        """ Test that a QuotationNotFound is raised when unsupported languages or quotations requested """
        from errors import LanguageNotSupported, QuotationNotFound

        # klingon should not be supported, maybe in the future?
        self.assertRaises(LanguageNotSupported, Quotation.__call__, "klingon", 10)

        # french should not include japanese quotation
        self.assertRaises(QuotationNotFound, Quotation.create, constants.LC_FRENCH, u"「")

    def test_create(self):
        """ Test that a Quotation.create works when supported language and quotation character """
        tests = [
            {"lc": constants.LC_FRENCH, "char": u"«"},
            {"lc": constants.LC_ENGLISH, "char": u"\"", "close": True},
            {"lc": constants.LC_JAPANESE, "char": u"「"}
        ]

        for test in tests:
            q = Quotation.create(test["lc"], test["char"], force_close=("close" in test))
            self.assertTrue(q)
            self.assertEqual(str(q), test["char"].encode('utf-8'))

    def test_mirror(self):
        """ Test that a QuotationNotFound is raised when unsupported languages or quotations requested """
        from errors import QuotationNotFound
        tests = [
            {"opening": u"„", "closing": u"“", "lc": constants.LC_GERMAN},
            {"opening": u"『", "closing": u"』", "lc": constants.LC_CHINESE}
        ]

        for test in tests:
            opening = Quotation.create(test["lc"], test["opening"])
            closing = opening.mirror()
            self.assertTrue(str(closing), test["closing"])
            self.assertTrue(opening ^ closing)


class TestQuotationValid(unittest.TestCase):

    def test_validate_success(self):
        """ Test to check that translation's quotations open and close correctly."""
        tests = [
            {
                "source": u"'Hello world,' she said.",
                "translation": u"«Bonjour tout le monde», dit-elle.",
                "language_pair": "{}_{}".format(constants.LC_ENGLISH, constants.LC_FRENCH)
            },
            {
                "source": u"'Hello world,' she said.",
                "translation": u"「世界こんにちは」と彼女は言いました。",
                "language_pair": "{}_{}".format(constants.LC_ENGLISH, constants.LC_JAPANESE)
            },
            {
                "source": u"this is a markdown text where we have a [link (please click)](https://www.google.com)",
                "translation": u"Ceci est un texte de démarque où nous avons un  [lien(s'il vous plaît cliquer sur)](https://www.google.com)",
                "language_pair": "{}_{}".format(constants.LC_ENGLISH, constants.LC_FRENCH)
            },
            {
                "source": u"「これは最高なものです！」と、彼女は叫びました",
                "translation": u"'This is dog's bollocks!', she exclaimed",
                "language_pair": "{}_{}".format(constants.LC_JAPANESE, constants.LC_ENGLISH),
                "remarks": "this is a more complicated test that lone rangers should be ignored (e.g., \"Maccabees' place \""
            },
            {

                "source": u"\"She said 'hello' to me the other day,\", Marie exclaimed.",
                "translation": u"『彼女は先日私に「こんにちは」を言った、』、マリーは叫びました。",
                "language_pair": "{}_{}".format(constants.LC_JAPANESE, constants.LC_ENGLISH),
                "remarks": "this is to test for nested quotations."
            }
        ]

        for i, test in enumerate(tests):
            ok, e = QuotationValidator.validate(test["source"], test["translation"], test["language_pair"], verbose=True)
            self.assertEqual(ok, True, msg="{} {}".format(i, str(e)))

    def test_validate_strict_success(self):
        """ Test to check that source and translation have equal amount and order of quotations """

        tests = [
            {
                "source": u"'Hello world,' she said.",
                "translation": u"«Bonjour tout le monde», dit-elle.",
                "language_pair": "{}_{}".format(constants.LC_ENGLISH, constants.LC_FRENCH)
            },
            {
                "source": u"'Hello world,' she said.",
                "translation": u"「世界こんにちは」と彼女は言いました。",
                "language_pair": "{}_{}".format(constants.LC_ENGLISH, constants.LC_JAPANESE)
            },
            {
                "source": u"this is a markdown text where we have a [link (please click)](https://www.google.com)",
                "translation": u"Ceci est un texte de démarque où nous avons un  [lien(s'il vous plaît cliquer sur)](https://www.google.com)",
                "language_pair": "{}_{}".format(constants.LC_ENGLISH, constants.LC_FRENCH)
            },
            {
                "source": u"「これは最高なものです！」と、彼女は叫びました",
                "translation": u"'This is dog's bollocks!', she exclaimed",
                "language_pair": "{}_{}".format(constants.LC_JAPANESE, constants.LC_ENGLISH),
                "remarks": "this is a more complicated test that lone rangers should be ignored (e.g., \"Maccabees' place \""
            },
            {
                "source": u"""
Bicycle Pumps


The bike pump can be complicated, too much so - valves, pressure adaptors and then there’s the whole CO2 thing. Our carefully chosen selection will help you find a mini pump to last a lifetime. So next time you're out of luck and fixing a puncture in the rain you will be back in the saddle in no time, confident that your tyre is as good as if you changed it on a sunny Sunday morning, tea in hand.

[[[google meta]]]

Buy Bicycle Pumps at Always Riding, from bike mini pumps to micro track pumps ideal for touring they all have fast, worldwide delivery direct to your door.




PDW Little Silver Mini Pump

PDW have taken the essential mini pump and made it into one good looking piece of kit. A CNC machined head, forged lock lever and bamboo handle combine to make this mini pump fit for even your prized ride.

Despite such an attractive exterior the Little Silver Mini Pump easily inflates Presta or Schrader valves on road and city bike tyres. Weighing in at only 85 grams, this little guy won’t add unnecessary heft to your steed.

    High pressure/low volume pump
    Includes alloy bracket for fastening to bike frame
    190mm long
    85 grams


[[[google meta]]]

Buy the PDW Little Silver Mini Pump from Always Riding, and enjoy fast, worldwide delivery to your door.




Crank Brothers Sterling Short Mini Pump

The Crank Brothers Sterling SG Pump uses a short, dual piston to maximise the amount of air pumped in with each compression. Using an air switch the Sterling SG can be changed from a high volume  (big tyres, lots of air), to high pressure (thin race tyres, high PSI) making it an essential whether on the road or trail.

Made using 6061 aluminium you can rest assured this pump is tough and will be ready for action when that unfortunate puncture occurs. The addition of a PSI gauge makes a real difference road side and removes the testing of the tyres and any subsequent dismounts to put a little more air in the tyre.

    141 grams
    6061 Aluminium
    PSI gauge
    Air switch to convert from high pressure to high volume
    198mm



[[[google meta]]]

Buy the PDW Little Silver Mini Pump from Always Riding, and enjoy fast, worldwide delivery to your door.




Lezyne Micro Floor Drive Pump HP


The Lezyne Micro Floor Pump is the perfect partner for long day rides or touring adventures. Track pump performance and power combine in this bike mini pump size to fit easily in a rucksack, bike bag or pannier.

CNC machining keeps wight low and durability high whilst a stainless steel foot peg provides stability and a floor pump feel while inflating. A rubber hose makes pumping easy whilst a double sided chuck assures compatibility with both Presta and Schraeder valves. A vital pressure gauge is a welcome touch to prevent the guessing game of how the tyre ‘feels’ with a little squeeze. Save your squeezing for your loved one.

    CNC machined
    Stainless steel foot peg
    Rubber hose for easy access
    Presta and Schraer compatible chuck
    Pressure gage
    194 grams



[[[google meta]]]

Buy the Lezyne Micro Floor Drive Pump HP from Always Riding, and enjoy fast, worldwide delivery to your door.




Inside Line Equipment Default Bag - XPAC


The Inside Line Default XPAC uses the same fabric that can be found on ILE's Race Day Bag. Originally a sail cloth, XPAC is something of a wonder fabric - rigid, super light and ripstop. Woven in Putnam Connecticut and made in California makes the Default XPAC a true US export.

The shape of the bag is the same as its Cordura sibling: a waterproof main compartment; hidden laptop sleeve; 25 litre capacity; adjustable sternum, waist, back and shoulder straps; easy access side pockets and all manner of front pockets. Coated zips add in extra water resistance whilst subtle ILE branding finish this feature laden bag.

Dimensions (H x W x D cm): 50 x 30 x 15
Volume: 25 litre
Laptop storage - up to 17" for main compartment, middle sleeve fits MacBook Air
Handmade in California
Weatherproof main compartment
Weatherproof hidden sleeve Adjustable/removable sternum and waist straps XPAC Sailcloth material
Water-resistant urethane coated zippers
Thick padded back and shoulder straps


[[[google meta]]]

Buy the Inside Line Equipment Default Bag - XPAC from Always Riding, and enjoy fast, worldwide delivery to your door.



Inside Line Equipment Phone Holster

Simple velcro straps attach the Inside Line Equipment Phone Holster to your ILE bag, allowing you to keep your phone or a point and shoot camera to hand at a moment's notice. Ample space for smartphones and a water resistant construction makes this a handy little addition to your ride attire.

Made in the USA the Phone Holster is made using a 1000D Cordura Nylon - the super tough stuff that many of Inside Line's bags are made from.

Compatible with iPhone/Samsung Galaxy
Elastic pen loops
Velcro straps
1000D Cordura Nylon



[[[google meta]]]

Buy the Inside Line Equipment Phone Holster from Always Riding, and enjoy fast, worldwide delivery to your door.




Cinelli Columbus Musette

Made in Italy from durable cotton fabric the Cinelli Columbus Musette adds some steel loving style to a ride where a jersey pocket just isn’t enough. A button closure keeps all your essentials safely inside allowing you to enjoy your city ride or open road adventure.

    30 x 40cm
    Made in Italy
    Button closure


[[[google meta]]]

Buy the Cinelli Columbus Musette from Always Riding, and enjoy fast, worldwide delivery to your door.



Birzman Belly S Top Tube Bag


For long days in the saddle, whether on a sportive, touring adventure or audax, having a few essentials easily to hand can make all the difference. A velcro closure provides easy access allowing you to carry say, short finger gloves for when the dawn sun begins to warm, or that burnout preventing flapjack or gel.

    13 x 6 x 4.5cm
    Rain cover
    Velcro closure


[[[google meta]]]

Buy the Birzman Belly S Top Tube Bag from Always Riding, and enjoy fast, worldwide delivery to your door.



Chrome Bravo Backpack


The Chrome Bravo Backpack is one of a new line of roll-top backpacks from this trail-blazing US brand that feature waterproof seam-welded inner compartments, up to 15" dedicated laptop storage, and volume adaptive expansion.

Pretty much a e'do it all' backpack for city cycling, the Chrome Bravo can transport everything from a 15" laptop (padded sleeve included of course), an iPad, U-lock, Kryptonite cable, jacket, lights, spare tubes, and pretty much anything else you can think of. Once packed, there is of course still room for more - loosen off the compression straps, extend the top and the Bravo doubles in size to 40L. To alleviate any discomfort caused by a lumpy load (dreaded carton corners can be particularly painful in a backpack), the backpack also includes a back frame sheet.


Features

    Waterproof compact urban daypack expands to double the capacity
    Dedicated laptop compartment to fit up to a MacBook Pro 15" computer
    Utility cross lashing straps to secure large haul items
    Waterproof external zippered front compartment
    Industrial strength Velcro accessory shoulder mounting strap
    Reinforced back panel for added support when fully loaded
    Ergonomic shoulder strap design with EVA foam back panel for improved fit and breathability
    Sternum strap for load distribution
    Industrial metal cam lock under arm compression buckles

Fabrication

    Weatherproof 1000 denier Cordura outer shell
    Waterproof 1800 denier military grade truck tarpaulin liner with bar welded seams
    Weatherproof urethane coated YKK zippers
    Dimensions (D x W x H) CM:  14 x 34.9 x 51.43


[[[google meta]]]

Buy the Chrome Bravo Backpack from Always Riding, and enjoy fast, worldwide delivery to your door.



Chrome Folsom Trouser

Chrome's Folsom Trousers feature the world renowned Schoeller fabric - tough, durable, water resistant downright ideal for cycling trousers. Designed for everyday riding these are a trouser suited equally to wet dirty rides as to warm summer cruises.

Finished with a seamless gusseted crotch and reinforced seams the Folsom Pants continue Chrome's mantra of bombproof design. Reflective details and reinforced belt loops add additional practicalities whilst a 5 bar webbing u-lock holster provides storage for a u-lock.

    4 Way Stretch Fabric
    Schoeller
    Gusseted Crotch


[[[google meta]]]

Buy the Chrome Folsom Trouser from Always Riding, and enjoy fast, worldwide delivery to your door.



Chrome Folsom Short


Made with a shorter, slimmer fit than the Chrome Union Short the Folsom Shorts have an 28cm inseam making them ideal for long summer rides and sunny city spins. Made using an Everest 4-way stretch fabric the Folsom, like the whole Chrome range, are tough. The four way stretch makes them perfect for everyday riding whilst a seamless gusseted crotch and reinforced seams ensure the kind of durability and longevity riders have come to expect from Chrome.

Finishing details come in the form of a reflective tag and reinforced belt loops whilst Chrome's signature use of 5-bar webbing features to provide a holster for the ever essential U-Lock.

    4 Way Stretch Fabric
    Everest Material
    Gusseted Crotch


[[[google meta]]]

Buy the Chrome Folsom Short from Always Riding, and enjoy fast, worldwide delivery to your door.




Chrome Victor Urban Utility Belt


Worn around the chest or waist the Victor Utility Belt provides additional functionality and storage for city cycling, urban adventures or touring. Enough space to house daily essentials plus a windbreaker or rain cape the Victor Utility Belt can also be used to carry an iPad mini.

Made in the USA and built tough to withstand inclement weather the Victor also features Chrome's signature buckle with an additional mounting loop for a carabineer or light.

    Padded Cordura fabric
    Chrome signature buckle
    Mounting loop
    Reflective elements
    Made in the USA.


[[[google meta]]]

Buy the Chrome Victor Urban Utility Belt from Always Riding, and enjoy fast, worldwide delivery to your door.



Chrome Messenger Organiser


 Slipped and securely fastened inside any Chrome Mini Metro, Citizen or Metropolis Messenger Bag, the Chrome Messenger Organiser instantly adds enhanced storage capabilities with space for A4 folders, a zippered pocket, quick access smartphone pocket and a notebook/moleskin pocket, all wrapped up in an easy to locate red exterior.

    Main pocket fits A4 size documents
    Zippered pocket to safely store personal items
    Cell phone pocket for quick access
    Small notebook/moleskin pocket
    Dimensions (cm): 25 x 35.5 x 0.6
    Integrates with interior Velcro lash mounting system for Chrome Mini Metro, Citizen, and Metropolis Messenger Bags
    Red truck tarpaulin exterior for visibility inside a dark bag
    Enhanced organisation and document protection
    Weatherproof 18oz truck tarpaulin construction
    Note: Made in Chico, California



[[[google meta]]]

Buy the Chrome Messenger Organiser from Always Riding, and enjoy fast, worldwide delivery to your door.



Chrome Union Shorts


Tailored with an updated slim cut, and built with proven urban cycling features like a lightweight, 4-way stretch water repellant fabric, lock down rear pocket, reflective logo,  gusseted crotch and deep front pockets, the Chrome Union Shorts are an ideal about town cycling short, styled for both on and off the bike adventures.

    Water resistant, durable 4-way stretch fabric for fit and movement
    Snap secured rear pocket keep your stuff in place
    Front coin pocket
    Mesh lined pockets
    Full-length gusset for on-the-bike comfort



[[[google meta]]]

Buy the Chrome Union Shorts from Always Riding, and enjoy fast, worldwide delivery to your door.




Chrome Sotnik Duffle Bag


 Part of the Chrome WWII-inspired Militia line, the Chrome Sotnik Duffle Bag is a 45-65l capacity bag, carried by hand, shoulder or simply pack style by generous haul straps.

Featuring a 100% welded-waterproof main compartment for total water ingress protection, it also sports a zippered compartment to keep wet/dry kit separate - a nice touch for beach days or post-bike kit changes at events. Outside pockets trimmed with stainless steel hardware ideal for storing small items complete the bag.

    Generous carry straps enable hand, shoulder or pack hauling
    Reinforced bottom straps for skateboard or large items
    Dimensions (cm): 30 x 50 x 25
    Volume: 45-65 L
    Weight: 3.9 lb / 1.7
    Waterproof rolltop closure accommodates a range of load sizes
    Welded internal bucket liner prevents water ingress
    External pockets with stainless steel hardware for quick secure access to u-lock and work tools
    Side straps designed to carry skateboard or large items
    Reinforced haul straps can be carried one handed or worn as backpack straps
    Weatherproof 1000 denier Cordura grade nylon outer shell
    Waterproof 1800 denier military grade truck tarpaulin liner with bar welded seams
    Built in: Chico, CA



[[[google meta]]]

Buy the Chrome Sotnik Duffle Bag from Always Riding, and enjoy fast, worldwide delivery to your door.



Brooks Leather Bar Tape

Befitting of a prized gran fondo, randonneur or vintage racing bike, Brooks Bar Tape adds Brooks' unrivalled heritage and leather expertise to this essential contact point. Made from a perforated leather that allows the tape to form to the bars over time, it also has the advantage of providing long lasting toughness; a trait epitomised in Brooks' Saddles.

Black, Honey, Brown Tapes made in Italy
Perforated Leather

What's in the box:

    2 Strips of perforated leather bar tape
    2 cork and wood bar plugs
    2 adhesive cloth strips


[[[google meta]]]

Buy the Brooks Leather Bar Tape from Always Riding, and enjoy fast, worldwide delivery to your door.




Brooks Slender Bar Grips


 Slender Grips are designed for flat bar users, and feature a cork tape grip that has been wrapped in traditional Brooks leather. Like many Brooks products when the Slender Grips get worn many of the parts can simply be replaced.

The tape is wrapped around the aluminium shell and is held in place by aluminium and steel clamps. In the event that the tape is worn, these can simply be removed and new tape rewound.

    Length: 130mm
    Inner Diameter 22.2mm
    Brooks Vegetable Tanned Leather
    Made in Italy


[[[google meta]]]

Buy the Brooks Slender Bar Grips from Always Riding, and enjoy fast, worldwide delivery to your door.



Brooks Brick Lane Roll-Up Panniers


Made in Italy from Brooks' water resistant cotton and finished with leather trim the Brick Lane Panniers are a throw back to the roll up bags featured in the 1890's Brooks catalogue.

Designed to stay on the bike, they can be easily rolled up when not in use and unrolled to provide extra storage for those days when you seem to return home with more than you set off with.

These Brooks panniers are also tailored with crossed elastic on the top to fasten particular bulky or mucky items to.

    Fastens to most racks with a width between 10 and 15 cm
    Volume per side 14 litres
    Total Volume 28 litres
    Total weight 950 g
    Width 34 cm
    Heigh 36 cm
    Depth 10 cm


[[[google meta]]]

Buy the Brooks Brick Lane Roll-Up Panniers from Always Riding, and enjoy fast, worldwide delivery to your door.



Solo CC Short Sleeve Jersey

porting a large Solo logo proudly positioned front and rear, the new Solo CC Jersey is a pared down, 1960s styled road cycling jersey available in three eye-catching dual-tone colours.

A more race fit than is offered through the New Zealand brand’s Classique line, and hence ideally suited to sportive, fast club run or road race adventures, the Solo CC Jersey is made from a Breathe functional fabric ideally suited to the rigours of cycling. Fashioned with a full zip and soft lycra arm bands, the CC includes 3 large elasticated rear pockets to provide ample space for snacks and supplies, and one smaller zipped pocket for keys/credit cards.

    Breathable with excellent moisture wicking capability
    Easy care, lightweight and quick drying
    Complete with an anti-bacterial treatment to minimise odour
    Full length zip
    Soft lycra arm bands for comfort and a side panel construction
    3 large elasticated rear pockets and one smaller zipped rear pocket



[[[google meta]]]

Buy the Solo CC Short Sleeve Jersey from Always Riding, and enjoy fast, worldwide delivery to your door.



[[[some terms and conditions text]]]


All UK orders are despatched as standard with a Royal Mail Tracked 48-hr service, but we do also offer an economic DPD next day service for more pressing orders.

Free UK Returns

All UK orders benefit from completely free returns. Inside your package you will find a returns pre-paid Royal Mail label, allowing you to pop the package into your local post office, or your work mail collection easily and hassle free. Returns take 48 hours to get back to us, and are fully tracked for your peace of mind.


[[[ email - abandoned cart]]]

[[[customer first name]]], did you forget to checkout?

Hey [[[customer first name]]]!

We couldn't help but notice that you left a few items in your shopping bag. If you would like to pick up where you left off, you can log in via this URL and go straight to checkout:

http://www.alwaysriding.co.uk/loginurl.html?access_token=1043_d7c73a9b0bc9f163ed65015204a226aa&redirect=aHR0cDovL3d3dy5hbHdheXNyaWRpbmcuY28udWsvc2hvcHBpbmdfY2FydC5odG1s

Do you have a question you'd like answering before you order? Remember, we're here to help, just reply to this email and we'll get you rolling before you know it.

The Always Riding Team
                """,
                "translation": u"""
Pompes à vélo

Les pompes à vélo peuvent être trop compliquées : les valves, les adaptateurs et tout le truc du CO2. Notre sélection habilement composée vous aidera à trouver une mini-pompe qui tiendra toute la vie. La prochaine fois que vous n’aurez pas de chance et que vous réparerez un pneu crevé sous la pluie, vous serez à nouveau en selle en un rien de temps, certain que votre pneu est en aussi bon état que si vous l’aviez changé en plein soleil un dimanche matin avec une tasse de thé à côté.

[[[google meta]]]

Achetez des pompes à vélo sur Always Riding, des mini-pompes aux pompes micro track, idéales pour le tourisme. Elles sont toutes livrées rapidement à domicile, partout dans le monde.




Mini-pompe PDW Little Silver

PDW a pris l’essentiel de la mini-pompe et en a fait un bel objet. Un crochet en alliage, usiné en CNC et un manche en bambou sont combinés pour faire une mini-pompe qui conviendra pour votre parcours préféré.

Malgré une apparence si attractive, cette mini-pompe Little Silver remplit facilement des valves Presta ou Shrader, sur des pneus de route ou de ville. Elle pèse à peine 85 grammes et n’ajoutera pas de poids inutile à votre monture.

Pompe haute pression/petit volume
Avec un crochet en alliage pour attacher au cadre vélo
190 mm de long
85 grammes

[[[google meta]]]

Achetez une mini-pompe PDW Little Silver sur Always Riding et profitez d’une livraison rapide à domicile, partout dans le monde.




Mini-pompe Crank Brothers Sterling Short

La pompe Crank Brothers Sterling SG utilise un piston court double pour maximiser le volume d’air introduit pendant chaque compression. Avec un sélecteur, la Sterling SG peut favoriser les gros volumes (gros pneu, beaucoup d’air) ou les hautes pressions (pneus fins de course, gros PSI), devenant un indispensable pour la route ou le trail.

Fait en aluminium 6061, vous pouvez être sûr que cette pompe solide sera prête à l’action quand cette crevaison imprévue surviendra. L’ajout d’une jauge PSI fait la différence sur le bord de la route et rend inutile le test des pneus et tout démontage pour ajouter plus d’air dans le pneu.

141 grammes
Aluminium 6061
Jauge PSI
Convertisseur d’air haute pression/gros volume
198 mm

[[[google meta]]]

Achetez une mini-pompe Crank Brothers Sterling Short sur Always Riding et profitez d’une livraison rapide à domicile, partout dans le monde.






Pompe à entraînement Lezyne Micro Floor HP

La pompe Lezyne Micro Floor est votre partenaire parfait pour les longues sorties à la journée ou les aventures de tourisme. La performance et la puissance de la pompe se combinent dans cette petite pompe pour entrer dans un sac à doc, un sac de vélo ou un panier.

L’usinage CNC maintient un faible poids et une bonne durabilité alors qu’un repose-pied en acier inoxydable offre stabilité et sensation de la pompe lors du gonflage. Un tuyau en caoutchouc facilite le pompage alors qu’un mandrin double assure la compatibilité entre les valves Presta et Schraeder. Une jauge de pression vitale est un ajout bienvenu pour éviter le petit jeu où l’on palpe le pneu pour deviner sa pression. Palpez plutôt ceux que vous aimez.

Usinage mécanique CNC
Repose-pied en acier inoxydable
Tuyau en caoutchouc pour un accès facile
Mandrin compatible Presta et Schraer
Jauge de pression
194 grammes

[[[google meta]]]

Achetez une pompe à entraînement Lezyne Micro Floor HP sur Always Riding et profitez d’une livraison rapide à domicile, partout dans le monde.






Sac Inside Line Equipment - XPAC

Le Inside Line Default XPAC utilise le même tissu que sur le sac Race Day de ILE. Le XPAC était à l’origine un tissu de marine, il est rigide, très léger et anti-déchirure. Tissé à Putnam dans le Connecticut et fait en Californie ; c’est un vrai produit d’export américain.

La forme du sac est la même que pour son cousin le Cordura : un compartiment principal étanche ; un étui à ordinateur caché ; une capacité de 25 litres ; une bandoulière ajustable sur le devant, la taille, le dos et les épaules ; des poches facilement accessibles sur les côtés et des poches à l’avant. Des fermetures éclairs vitrifiées ajoutent une étanchéité supérieure à ce sac à la touche subtile ILE.

Dimensions (H x W x D cm): 50 x 30 x 15
Volume : 25 litres
Stockage d’ordinateur – jusqu’à 17" pour le compartiment principal, la poche au milieu accueille un MacBook Air
Fait main en Californie
Compartiment principal étanche
Poche cachée étanche
Bandoulières ajustables/amovibles, toile de voile XPAC
Fermetures éclair vitrifiées étanches
Dos et bandoulière rembourrés

[[[google meta]]]

Achetez un sac Inside Line Equipment - XPAC sur Always Riding et profitez d’une livraison rapide à domicile, partout dans le monde.




Étui pour téléphone Inside Line Equipment

Des velcros attachent votre étui pour téléphone Inside Line Equipement à votre sac ILE, vous permettant de garder votre téléphone ou un appareil photo à portée de main. Grand espace pour les smartphones et construction étanche pour un ajout pratique à votre attirail de course.

Fabriqué aux États-Unis, l’étui pour téléphone est fait en nylon Cordura 1000D – le matériau très solide dans lequel la plupart des sacs Inside Line sont faits.

Compatible avec iPhone/Samsung Galaxy
Boucle élastique pour stylo
Bandoulière velcro
1000D Cordura Nylon

[[[google meta]]]

Achetez un étui pour téléphone Inside Line Equipment sur Always Riding et profitez d’une livraison rapide à domicile, partout dans le monde.






Cinelli Columbus Musette

Fabriqué en Italie à partir d’un tissu en coton durable, le Cinelli Colombus Musette ajoute un style acier à une course où la poche d’un maillot ne suffit pas. Une fermeture à bouton garde l’essentiel de vos affaires à l’abri, vous permettant de profiter de votre course en ville ou de votre aventure à l’air libre.

30 x 40 cm
Fabriqué en Italie
Fermeture par bouton

[[[google meta]]]

Achetez un Cinelli Columbus Musette sur Always Riding et profitez d’une livraison rapide à domicile, partout dans le monde.



Sac de cadre Birzman Belly S

Pour de longues journées sur la selle, pour une aventure de tourisme sportive, le fait d’avoir vos affaires indispensables à portée de main peut faire toute la différence. Une fermeture velcro offre un accès facile pour vous permettre de porter par exemple des gants courts pour le lever du jour, ou ces biscuits et gels énergétiques.

13 x 6 x 4.5 cm
Couvercle
Fermeture velcro

[[[google meta]]]

Achetez un sac de cadre Birzman Belly S sur Always Riding et profitez d’une livraison rapide à domicile, partout dans le monde.




Sac à dos Chrome Bravo

Le sac à dos Chrome Bravo est l’un des nouveaux sac à dos de cette marque américaine incroyable, avec des compartiments à coutures soudées étanches, avec un espace pour ordinateurs portables 15’’, et un volume adaptatif.

Le Chrome Bravo est un sac à dos polyvalent pour le vélo en ville, il peut tout transporter, un ordinateur portable 15’’ (poche rembourrée incluse), un iPad, un antivol, un câble Kryptonite, une veste, des lumières, des chambres à air de rechange, et tout ce à quoi vous pouvez penser. Une fois emballé, il y a bien sûr de la place pour plus – ouvrez les fermetures, étendez le haut et le Bravo double sa taille pour 40 L. Pour soulager tout inconfort dû à une charge irrégulière (les coins des cartons peuvent faire particulièrement mal), le sac à dos comprend un tissu à la forme du dos.



Caractéristiques

Ce sac de jour urbain compact étanche peut s’agrandir jusqu’à doubler sa capacité
Compartiment d’ordinateur portable dédié pour accueillir un ordinateur MacBook Pro 15’’
Bandoulière croisée pour sécuriser les objets sur de longues distances
Compartiment avant extérieur étanche à fermeture éclair
Bandoulière à accessoires à Velcro de force industrielle
Panneau renforcé pour un meilleur support quand le sac est plein
Design de bandoulière ergonomique rembourrée en mousse EVA pour une coupe améliorée et une bonne aération.
Bandoulière pour distribuer la charge
Serrure à levier en métal industriel

Fabrication

Coque extérieure étanche en Cordura 1000 deniers
Doublure étanche en bâche militaire 1800 deniers avec coutures soudées
Fermeture éclair vitrifiée étanche YKK
Dimensions (D x W x H) cm : 14 x 34,9 x 51,43

[[[google meta]]]

Achetez un sac à dos Chrome Bravo sur Always Riding et profitez d’une livraison rapide à domicile, partout dans le monde.




Pantalon Chrome Folsom

Le pantalon Chrome Folson utilise le tissu Schoeller connu dans le monde entier – solide, durable, étanche : idéal pour un pantalon de vélo. Conçu pour des courses de tous les jours, ce pantalon convient aussi bien pour les sorties où on se salit que pour les balades en été.

Avec un entre-jambe à gousset sans couture et des coutures renforcées, le pantalon Folsom est dans la continuité des designs solides de Chrome. Des détails réfléchissants et des boucles de ceinture renforcées ajoutent du confort alors que ce porte-antivol 5 bar permet de stocker un antivol.

Tissu quadri-extensible
Schoeller
Entre-jambe à soufflet

[[[google meta]]]

Achetez un pantalon Chrome Folsom sur Always Riding et profitez d’une livraison rapide à domicile, partout dans le monde.




Short Chrome Folsom

Fabriqué plus court et plus fin que le short Chrome Union, le short Folsom a une couture de 28cm, idéale pour les longues sorties d’été et les balades en ville. En tissu quadri-extensible Everest, le Folsom, comme toute la gamme Chrome, est solide. Le tissu quadri-extensible est parfait pour les courses de tous les jours alors que l’entre-jambe à soufflet sans couture et les coutures renforcées assure la durabilité que les cyclistes attendent de Chrome.


Les finitions comprennent une étiquette réfléchissante et des boucles renforcées alors qu’un porte-antivol 5 bar permet de stocker un antivol.

Tissu quadri-extensible
Matériel Everest
Entre-jambe à soufflet

[[[google meta]]]

Achetez un short Chrome Folsom sur Always Riding et profitez d’une livraison rapide à domicile, partout dans le monde.







Ceinture de gadgets Chrome Victor Urban

Porté autour de la taille, la ceinture de gadgets offre des fonctionnalités et du stockage supplémentaires pour du vélo en ville, des aventures urbaines ou du tourisme. Avec suffisamment d’espace pour accueillir les essentiels de tous les jours, avec un coupe-vent ou une cape de pluie, la ceinture Victor peut aussi être utilisée pour porter un iPad mini.

Fabriqué aux USA et solide pour résister aux intempéries, la Victor a une boucle Chrome avec une boucle de montage supplémentaire pour un mousqueton ou une lumière.

Cordura capitonné
Boucle signature chromée
Boucle de montage
Éléments réfléchissants
Fabriqué aux USA

[[[google meta]]]

Achetez un ceinture de gadgets Chrome Victor Urban sur Always Riding et profitez d’une livraison rapide à domicile, partout dans le monde.




Organiseur besace Chrome

Glissée et accrochée en toute sécurité à l’intérieur de toute besace Chrome Mini Metro, Citizen ou Metropolis, l’organiseur besace Chrome ajoute instantanément une capacité de stockage améliorée avec de l’espace pour des dossiers A4, une poche à fermeture éclair, une poche avec accès rapide à un smartphone et une poche pour carnet/Moleskine, le tout enveloppé de rouge facile à détecter.

La poche principale accueille des documents A4
Poche à fermeture éclair pour stocker vos objets personnels en toute sécurité
Poche à téléphone mobile pour un accès rapide
Poche à Moleskine/petit carnet
Dimensions (cm): 25 x 35.5 x 0.6

S’intègre à un système de montage intérieur en velcro pour besaces Chrome Mini Metro, Citizen, et Metropolis
Bâche extérieure rouge pour être visible dans un sac sombre
Organisation améliorée et protection des documents
Fabriqué en bâche étanche 18oz
Note : Fabriqué à Chico, Californie

[[[google meta]]]

Achetez un organiseur besace Chrome sur Always Riding et profitez d’une livraison rapide à domicile, partout dans le monde.



Short Chrome Union

Taillé suivant une coupe lisse et construit avec des fonctionnalités prouvées pour le cyclisme, comme un tissu quadri-extensible léger et étanche, une poche arrière sécurisée, un logo réfléchissant, un entre-jambe à soufflet et des poches avant profondes, le short Chrome Union est un short idéal pour le vélo en ville, avec un style pour des aventures à vélo et à côté du vélo.

Tissu quadri-extensible durable et étanche pour une bonne liberté de mouvement
Poche arrière sécurisée pour garder vos affaires à leur place
Poche à pièces à l’avant
Poches doublées en maille
Entre-jambe à soufflet pour du confort à vélo

[[[google meta]]]

Achetez un short Chrome Union sur Always Riding et profitez d’une livraison rapide à domicile, partout dans le monde.







Sac de sport Chrome Sotnik

Faisant partie de la ligne Militia Chrome inspirée de la seconde guerre mondiale, le sac de sport Chrome Sotnik est un sac de capacité 45-65L, porté à la main, à l’épaule ou sur le dos par des sangles généreuses.

Avec un compartiment principal 100% étanche pour une protection totale à l’eau, il présente également un compartiment à fermeture éclair pour garder les affaires sèches et mouillées séparées – une touche sympathique pour les journées à la plage ou pour le change après le vélo. Les poches extérieures avec un cadre en inox sont idéales pour stocker des petits objets.

Bandoulière généreuse pour porter à la main, à l’épaule ou sur le dos
Sangles renforcées pour un skateboard ou de gros objets
Dimensions (cm) : 30 x 50 x 25
Volume : 45-65 L
Poids : 3.9 lb / 1.7
Fermeture étanche pour accueillir plusieurs charges
Doublure interne soudée pour empêcher la progression de l’eau
Poches extérieures avec cadre en inox pour un accès sûr à l’antivol ou à des outils de travail
Des sangles latérales conçues pour porter un skateboard ou de gros objets
Bandoulières renforcées pour porter à la main ou en sac à dos
Coque extérieure étanche en Cordura 1000 deniers
Doublure étanche en bâche militaire 1800 deniers avec coutures soudées
Fabriqué à Chico, CA

[[[google meta]]]

Achetez un sac de sport Chrome Sotnik sur Always Riding et profitez d’une livraison rapide à domicile, partout dans le monde.






Ruban de guidon en cuir Brooks

Conçu pour des vélos de course de grand fond, de randonneur ou vintage, le ruban de guidon Brooks apporte un héritage inégalé et une expertise du cuir à ce point de contact essentiel. Fait en cuir perforé qui permet au ruban de prendre la forme du guidon, il présente également l’avantage d’être résistant plus longtemps, un trait caractéristique des selles Brooks.

Rubans noir, miel et marron fabriqués en Italie
Cuir perforé

Contenu de la boîte :
2 rouleaux de ruban en cuir perforé
2 bouchons en liège et en bois
2 rubans adhésifs

[[[google meta]]]

Achetez le ruban de guidon en cuir Brooks sur Always Riding et profitez d’une livraison rapide à domicile, partout dans le monde.







Poignées fines Brooks

Les poignées fines sont conçues pour les guidons plats et sont enveloppées d’un cuir traditionnel Brooks. Comme pour beaucoup de produits Brooks pour lesquels les poignées fines s’abîment, la plupart des pièces peuvent être remplacées.

L’adhésif est enveloppé autour d’une coque en aluminium et est tenu en place par des pinces en aluminium et en acier. Au cas où l’adhésif serait abîmé, on peut simplement les enlever et replacer de l’adhésif.

Longueur : 130mm
Diamètre intérieur : 22.2mm
Cuir tanné végétal Brooks
Fabriqué en Italie

[[[google meta]]]

Achetez les poignées fines Brooks sur Always Riding et profitez d’une livraison rapide à domicile, partout dans le monde.




Paniers à rabats Brooks Brick Lane

Fabriqués en Italie en coton étanche Brooks et avec une finition en cuir, les paniers Brick Lane sont un rappel des sacs à rabats du catalogue Brooks des années 1890.

Conçus pour rester sur le vélo, ils peuvent être facilement enroulés quand ils ne sont pas utilisés, et déroulés pour fournir plus d’espace de stockage pour les jours où vous rentrerez avec plus d’affaires que quand vous êtes partis.

Ces paniers Brooks sont également conçus avec des élastiques croisés au sommet pour y attacher des objets volumineux.

S’attache à la plupart des racks avec une largeur entre 10 et 15 cm
Volume par côté 14 litres
Volume total 28 litres
Poids total 950 g
Largeur 34 cm
Hauteur 36 cm
Profondeur 10 cm

[[[google meta]]]

Achetez les paniers à rabats Brooks Brick Lane sur Always Riding et profitez d’une livraison rapide à domicile, partout dans le monde.





Maillot manches courtes Solo CC

Avec un grand logo Solo positionné fièrement à l’avant et à l’arrière, le nouveau maillot Solo CC est un maillot de vélo de route style 1960, disponible dans trois tons de couleurs tape-à-l’œil.

Avec une nouvelle coupe pour la ligne Classique de la marque néo-zélandaise, idéale pour les courses sportives ou les aventures sur la route, le maillot Solo CC est fait dans un tissu respirant fonctionnel adapté aux contraintes du cyclisme. Avec une fermeture éclair intégrale et des bandes en lycra aux bras, le CC comprend 3 grandes poches arrière élastiques pour fournir un grand espace pour les snacks et ravitaillements, et une poche à fermeture éclair plus petite pour les cartes de crédit et les clés.

Respirant avec une excellent capacité à évacuer l’humidité
Soin facilité, léger et séchage rapide
Avec un traitement antibactérien pour minimiser l’odeur
Fermeture éclair intégrale
Bandes en lycra aux bras pour du confort et un panneau latéral
3 grandes poches arrière élastique et un poche arrière plus petite à fermeture éclair

[[[google meta]]]

Achetez un maillot manches courtes Solo CC sur Always Riding et profitez d’une livraison rapide à domicile, partout dans le monde.



[[[some terms and conditions text]]]

Toutes les commandes vers le Royaume-Uni sont envoyées en standard avec le service suivi sous 48h de Royal Mail, mais nous proposons également un service économique DPD avec livraison le lendemain pour les commandes plus urgentes.

Retours gratuits au Royaume-Uni

Toutes les commandes vers le Royaume-Uni peuvent être renvoyées gratuitement. Vous trouverez dans votre colis une étiquette prépayée Royal Mail qui vous permettra de déposer votre colis au bureau de poste, ou au service courrier de votre travail, facilement et sans tracas. Les retours nous parviennent sous 48h et sont suivies pour votre tranquillité d'esprit.


[[[ email - abandoned cart]]]

[[[customer first name]]], avez-vous oublié de finaliser votre commande ?

Bonjour [[[customer first name]]] !

Nous n'avons pas pu nous empêcher de remarquer qu'il reste quelques objets dans votre panier. Si vous voulez reprendre là où vous en êtes resté, veuillez vous connecter à l'URL suivante pour finaliser votre commande :

http://www.alwaysriding.co.uk/loginurl.html?access_token=1043_d7c73a9b0bc9f163ed65015204a226aa&redirect=aHR0cDovL3d3dy5hbHdheXNyaWRpbmcuY28udWsvc2hvcHBpbmdfY2FydC5odG1s

Avez-vous des questions à poser avant de commander ? Souvenez-vous que nous sommes là pour aider, répondez à cet e-mail et nous vous répondrons aussi vite que possible.

L'équipe Always Riding
                """,
                "language_pair": "{}_{}".format(constants.LC_ENGLISH, constants.LC_FRENCH),
                "remarks": "big ass text!"
            }
        ]

        for i, test in enumerate(tests):
            ok, e = QuotationValidator.validate(test["source"], test["translation"], test["language_pair"], strict=True, verbose=True)
            self.assertEqual(ok, True, msg=str(e))

    def test_validate_strict_failure(self):
        """ Test to check that source and translation have equal amount and order of quotations """
        pass

if __name__ == "__main__":
    unittest.main()
