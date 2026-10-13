"""
Complete Kenya Administrative Locations
47 Counties → Sub-Counties → Wards → Constituencies
"""

# Complete hierarchical structure
KENYA_LOCATIONS = {
    "Mombasa": {
        "sub_counties": {
            "Changamwe": {
                "wards": ["Changamwe", "Port Reitz", "Kipevu", "Airport", "Chaani"],
                "constituencies": ["Changamwe"]
            },
            "Jomvu": {
                "wards": ["Jomvu Kuu", "Miritini", "Mikindani"],
                "constituencies": ["Jomvu"]
            },
            "Kisauni": {
                "wards": ["Mjambere", "Junda", "Bamburi", "Mwakirunge", "Mtopanga", "Magogoni", "Shanzu"],
                "constituencies": ["Kisauni"]
            },
            "Likoni": {
                "wards": ["Mtongwe", "Shika Adabu", "Bofu", "Likoni", "Timbwani"],
                "constituencies": ["Likoni"]
            },
            "Mvita": {
                "wards": ["Mji wa Kale/Makadara", "Tudor", "Tononoka", "Shimanzi/Ganjoni", "Majengo"],
                "constituencies": ["Mvita"]
            },
            "Nyali": {
                "wards": ["Frere Town", "Ziwa la Ng'ombe", "Mkomani", "Kongowea", "Kadzandani"],
                "constituencies": ["Nyali"]
            }
        }
    },
    
    "Kwale": {
        "sub_counties": {
            "Msambweni": {
                "wards": ["Gombato Bongwe", "Ukunda", "Kinondo", "Ramisi"],
                "constituencies": ["Msambweni"]
            },
            "Lunga Lunga": {
                "wards": ["Pongwe/Kikoneni", "Dzombo", "Mwereni", "Vanga"],
                "constituencies": ["Lunga Lunga"]
            },
            "Matuga": {
                "wards": ["Tsimba Golini", "Waa", "Tiwi", "Kubo South", "Mkongani"],
                "constituencies": ["Matuga"]
            },
            "Kinango": {
                "wards": ["Ndavaya", "Kinango", "Mackinnon Road", "Chengoni/Samburu", "Mwavumbo"],
                "constituencies": ["Kinango"]
            }
        }
    },
    
    "Kilifi": {
        "sub_counties": {
            "Kilifi North": {
                "wards": ["Tezo", "Sokoni", "Kibarani", "Watamu", "Mnarani", "Shimo La Tewa", "Chasimba"],
                "constituencies": ["Kilifi North"]
            },
            "Kilifi South": {
                "wards": ["Junju", "Mwarakaya", "Shimo La Tewa", "Mtepeni", "Mwanamwinga", "Chasimba"],
                "constituencies": ["Kilifi South"]
            },
            "Kaloleni": {
                "wards": ["Mariakani", "Kaloleni", "Mwanamwinga", "Jibana"],
                "constituencies": ["Kaloleni"]
            },
            "Rabai": {
                "wards": ["Ruruma", "Kambe/Ribe", "Kisurutini", "Rabai/Kisurutini", "Mwawesa"],
                "constituencies": ["Rabai"]
            },
            "Ganze": {
                "wards": ["Bamba", "Ganze", "Jaribuni", "Sokoke"],
                "constituencies": ["Ganze"]
            },
            "Malindi": {
                "wards": ["Malindi Town", "Shella", "Ganda", "Jilore", "Kakuyuni", "Gongoni", "Garsen"],
                "constituencies": ["Malindi"]
            },
            "Magarini": {
                "wards": ["Garsen South", "Garsen Central", "Garsen North", "Garsen West", "Kipini East", "Kipini West"],
                "constituencies": ["Magarini"]
            }
        }
    },
    
    "Tana River": {
        "sub_counties": {
            "Garsen": {
                "wards": ["Garsen South", "Garsen Central", "Garsen North", "Kipini East", "Kipini West"],
                "constituencies": ["Garsen"]
            },
            "Galole": {
                "wards": ["Wayu/Sankuri", "Chewani", "Mikinduni", "Kinakomba"],
                "constituencies": ["Galole"]
            },
            "Bura": {
                "wards": ["Bangale", "Sala", "Chewele", "Madogo", "Hirimani"],
                "constituencies": ["Bura"]
            }
        }
    },
    
    "Lamu": {
        "sub_counties": {
            "Lamu East": {
                "wards": ["Faza", "Kiunga", "Basuba"],
                "constituencies": ["Lamu East"]
            },
            "Lamu West": {
                "wards": ["Mkomani", "Hongwe", "Witu", "Bahari"],
                "constituencies": ["Lamu West"]
            }
        }
    },
    
    "Taita Taveta": {
        "sub_counties": {
            "Taveta": {
                "wards": ["Bomeni", "Chala", "Mahoo", "Mboghoni", "Mata"],
                "constituencies": ["Taveta"]
            },
            "Wundanyi": {
                "wards": ["Wundanyi/Mbale", "Werugha", "Wumingu/Kishushe", "Mbololo"],
                "constituencies": ["Wundanyi"]
            },
            "Mwatate": {
                "wards": ["Mwatate", "Ronge", "Bura", "Chawia", "Wusi/Kishamba"],
                "constituencies": ["Mwatate"]
            },
            "Voi": {
                "wards": ["Mbololo", "Sagalla", "Kaloleni", "Marungu", "Kasigau", "Ngolia"],
                "constituencies": ["Voi"]
            }
        }
    },
    
    "Garissa": {
        "sub_counties": {
            "Garissa Township": {
                "wards": ["Township", "Galbet", "Waberi", "Iftin/Nuno"],
                "constituencies": ["Garissa Township"]
            },
            "Balambala": {
                "wards": ["Saka", "Balambala", "Sankuri", "Danyere"],
                "constituencies": ["Balambala"]
            },
            "Lagdera": {
                "wards": ["Goreale", "Benane", "Sabena", "Shedder"],
                "constituencies": ["Lagdera"]
            },
            "Dadaab": {
                "wards": ["Damajale", "Labasigale", "Abakaile", "Dertu"],
                "constituencies": ["Dadaab"]
            },
            "Fafi": {
                "wards": ["Jarajila", "Fafi", "Nanighi", "Bura"],
                "constituencies": ["Fafi"]
            },
            "Ijara": {
                "wards": ["Hulugho", "Sangailu", "Ijara", "Masalani"],
                "constituencies": ["Ijara"]
            }
        }
    },
    
    "Wajir": {
        "sub_counties": {
            "Wajir North": {
                "wards": ["Danaba", "Gurar", "Batalu", "Burder", "Korondile"],
                "constituencies": ["Wajir North"]
            },
            "Wajir East": {
                "wards": ["Barwago", "Khorof/Harar", "Wajir Bor", "Wagberi"],
                "constituencies": ["Wajir East"]
            },
            "Tarbaj": {
                "wards": ["Tarbaj", "Wajir South", "Elben", "Diif"],
                "constituencies": ["Wajir South"]
            },
            "Wajir West": {
                "wards": ["Hadado/Athibohol", "Ademasajide", "Ganyure/Wagalla", "Eldas", "Lakoley South/Basir"],
                "constituencies": ["Wajir West"]
            }
        }
    },
    
    "Mandera": {
        "sub_counties": {
            "Mandera West": {
                "wards": ["Gither", "Lagsure", "Shimbir Fatuma", "Derkale"],
                "constituencies": ["Mandera West"]
            },
            "Mandera South": {
                "wards": ["Kutulo", "Malka", "Elwak South", "Elwak North"],
                "constituencies": ["Mandera South"]
            },
            "Mandera North": {
                "wards": ["Rhamu", "Rhamu Dimtu", "Ashabito", "Arabia"],
                "constituencies": ["Mandera North"]
            },
            "Mandera East": {
                "wards": ["Neboi", "Khalalio", "Banissa", "Kiliweheri"],
                "constituencies": ["Mandera East"]
            }
        }
    },
    
    "Marsabit": {
        "sub_counties": {
            "Moyale": {
                "wards": ["Golbo", "Moyale Township", "Obbu", "Uran", "Butiye"],
                "constituencies": ["Moyale"]
            },
            "North Horr": {
                "wards": ["North Horr", "Dukana", "Maikona", "Turbi", "Bubisa"],
                "constituencies": ["North Horr"]
            },
            "Saku": {
                "wards": ["Marsabit Central", "Karare", "Sagante/Jaldesa", "Kargi/South Horr"],
                "constituencies": ["Saku"]
            },
            "Laisamis": {
                "wards": ["Laisamis", "Korr/Ngurunit", "Logologo", "Loiyangalani"],
                "constituencies": ["Laisamis"]
            }
        }
    },
    
    "Isiolo": {
        "sub_counties": {
            "Isiolo North": {
                "wards": ["Wabera", "Bulla Pesa", "Chari"],
                "constituencies": ["Isiolo North"]
            },
            "Isiolo South": {
                "wards": ["Ngare Mara", "Sericho", "Kinna", "Oldonyiro", "Garba Tula"],
                "constituencies": ["Isiolo South"]
            },
            "Merti": {
                "wards": ["Cherab", "Kom  bole", "Chari"],
                "constituencies": ["Isiolo North"]
            }
        }
    },
    
    "Meru": {
        "sub_counties": {
            "Igembe South": {
                "wards": ["Akachiu", "Muthara", "Kanuni", "Athiru Ruujine", "Athiru Gaiti"],
                "constituencies": ["Igembe South"]
            },
            "Igembe Central": {
                "wards": ["Igembe East", "Kangeta", "Naathu", "Athiru Central"],
                "constituencies": ["Igembe Central"]
            },
            "Igembe North": {
                "wards": ["Antubetwe Kiongo", "Ntunene", "Antuambui", "Naathu"],
                "constituencies": ["Igembe North"]
            },
            "Tigania West": {
                "wards": ["Akithii", "Kianjai", "Nkomo", "Mbeu", "Nkuene"],
                "constituencies": ["Tigania West"]
            },
            "Tigania East": {
                "wards": ["Mikinduri", "Thangatha", "Muthara West", "Antugiria", "Karama"],
                "constituencies": ["Tigania East"]
            },
            "North Imenti": {
                "wards": ["Imenti Central", "Abothuguchi Central", "Municipality", "Abothuguchi West"],
                "constituencies": ["North Imenti"]
            },
            "Buuri": {
                "wards": ["Kisima", "Timau", "Kiirua", "Kiagu", "Ruiri"],
                "constituencies": ["Buuri"]
            },
            "Central Imenti": {
                "wards": ["Abogeta East", "Abogeta West", "Kiagu", "Mugwe", "Muthara East"],
                "constituencies": ["Central Imenti"]
            },
            "South Imenti": {
                "wards": ["Igoji East", "Igoji West", "Abothuguchi East", "Mitunguu", "Nkuene"],
                "constituencies": ["South Imenti"]
            }
        }
    },
    
    "Tharaka Nithi": {
        "sub_counties": {
            "Maara": {
                "wards": ["Chogoria", "Ganga", "Karingani", "Magumoni", "Mitheru"],
                "constituencies": ["Maara"]
            },
            "Chuka/Igambang'ombe": {
                "wards": ["Karingani", "Mugwe", "Magumoni", "Igambang'ombe", "Mariani"],
                "constituencies": ["Chuka/Igambang'ombe"]
            },
            "Tharaka": {
                "wards": ["Gatunga", "Nkondi", "Chiakariga", "Marimanti"],
                "constituencies": ["Tharaka"]
            }
        }
    },
    
    "Embu": {
        "sub_counties": {
            "Manyatta": {
                "wards": ["Gaturi South", "Kithimu", "Kirimari", "Gaturi North", "Ruguru/Ngandori"],
                "constituencies": ["Manyatta"]
            },
            "Runyenjes": {
                "wards": ["Kyeni North", "Kyeni South", "Kabare/Murungaa", "Central", "Gaturi South"],
                "constituencies": ["Runyenjes"]
            },
            "Mbeere South": {
                "wards": ["Mavuria", "Kiambere", "Mbeti South", "Makima"],
                "constituencies": ["Mbeere South"]
            },
            "Mbeere North": {
                "wards": ["Muminji", "Evurore", "Nthawa"],
                "constituencies": ["Mbeere North"]
            }
        }
    },
    
    "Kitui": {
        "sub_counties": {
            "Mwingi North": {
                "wards": ["Kyuso", "Mumoni", "Nguni", "Nuu"],
                "constituencies": ["Mwingi North"]
            },
            "Mwingi West": {
                "wards": ["Kyome/Thaana", "Ngomeni", "Kyethani", "Mumoni", "Kauwi"],
                "constituencies": ["Mwingi West"]
            },
            "Mwingi Central": {
                "wards": ["Central", "Kivou", "Ngonyi", "Waita", "Mwingi"],
                "constituencies": ["Mwingi Central"]
            },
            "Kitui West": {
                "wards": ["Kauwi", "Migwani", "Kiomo/Kyethani", "Mutitu"],
                "constituencies": ["Kitui West"]
            },
            "Kitui Rural": {
                "wards": ["Kisasi", "Mbitini", "Kwavonza/Yatta", "Kanyangi"],
                "constituencies": ["Kitui Rural"]
            },
            "Kitui Central": {
                "wards": ["Township", "Kyangwithya West", "Mulango", "Miambani"],
                "constituencies": ["Kitui Central"]
            },
            "Kitui East": {
                "wards": ["Zombe/Mwitika", "Endau/Malalani", "Mutito/Kaliku", "Ikanga/Kyatune"],
                "constituencies": ["Kitui East"]
            },
            "Kitui South": {
                "wards": ["Ikutha", "Mutomo", "Mutha", "Kiseini/Muumoni"],
                "constituencies": ["Kitui South"]
            }
        }
    },
    
    "Machakos": {
        "sub_counties": {
            "Masinga": {
                "wards": ["Ekalakala", "Muthesya", "Kivaa", "Masinga Central", "Ndithini"],
                "constituencies": ["Masinga"]
            },
            "Yatta": {
                "wards": ["Kithimani", "Ikombe", "Katangi", "Matungulu North", "Kola"],
                "constituencies": ["Yatta"]
            },
            "Kangundo": {
                "wards": ["Kangundo North", "Kangundo Central", "Kangundo East", "Kangundo West"],
                "constituencies": ["Kangundo"]
            },
            "Matungulu": {
                "wards": ["Tala", "Matungulu North", "Matungulu West", "Matungulu East", "Kyeleni"],
                "constituencies": ["Matungulu"]
            },
            "Kathiani": {
                "wards": ["Kathiani Central", "Lower Kaewa/Iveti", "Mitaboni", "Kathiani West"],
                "constituencies": ["Kathiani"]
            },
            "Mavoko": {
                "wards": ["Syokimau/Mulolongo", "Athi River", "Kinanie", "Muthwani"],
                "constituencies": ["Mavoko"]
            },
            "Machakos Town": {
                "wards": ["Muvuti/Kiima-Kimwe", "Mumbuni North", "Machakos Central", "Kalama"],
                "constituencies": ["Machakos Town"]
            },
            "Mwala": {
                "wards": ["Kibauni", "Makutano/Mwala", "Masii", "Muthetheni", "Mbiuni"],
                "constituencies": ["Mwala"]
            }
        }
    },
    
    "Makueni": {
        "sub_counties": {
            "Makueni": {
                "wards": ["Muvau", "Mavindini", "Nguumo", "Kathonzweni", "Mavoko"],
                "constituencies": ["Makueni"]
            },
            "Kibwezi West": {
                "wards": ["Emali/Mulala", "Nguumo", "Kikumbulyu North", "Kikumbulyu South"],
                "constituencies": ["Kibwezi West"]
            },
            "Kibwezi East": {
                "wards": ["Masongaleni", "Mtito Andei", "Ukia", "Nguni", "Thange"],
                "constituencies": ["Kibwezi East"]
            },
            "Kilome": {
                "wards": ["Kilome/Ikalyoni", "Kasikeu", "Mutha", "Ukia"],
                "constituencies": ["Kilome"]
            },
            "Kaiti": {
                "wards": ["Kalii", "Kee", "Kaiti Central", "Kithuki"],
                "constituencies": ["Kaiti"]
            },
            "Mbooni": {
                "wards": ["Tulimani", "Waia/Kako", "Mbooni", "Kalawa", "Kiteta/Kisau"],
                "constituencies": ["Mbooni"]
            }
        }
    },
    
    "Nyandarua": {
        "sub_counties": {
            "Kinangop": {
                "wards": ["Murungaru", "Gathara", "Magumu", "Njabini/Kiburu"],
                "constituencies": ["Kinangop"]
            },
            "Kipipiri": {
                "wards": ["Wanjohi", "Kipipiri", "Geta", "Githioro"],
                "constituencies": ["Kipipiri"]
            },
            "Ol Joro Orok": {
                "wards": ["Weru", "Gatimu", "Gathanji"],
                "constituencies": ["Ol Joro Orok"]
            },
            "Ol Kalou": {
                "wards": ["Karau", "Rurii", "Kaimbaga", "Mirangine"],
                "constituencies": ["Ol Kalou"]
            },
            "Ndaragwa": {
                "wards": ["Leshau/Pondo", "Kiriita", "Central", "Shamata"],
                "constituencies": ["Ndaragwa"]
            }
        }
    },
    
    "Nyeri": {
        "sub_counties": {
            "Tetu": {
                "wards": ["Aguthi/Gaaki", "Tetu", "Wamagana"],
                "constituencies": ["Tetu"]
            },
            "Kieni": {
                "wards": ["Mugunda", "Gatarakwa", "Thegu River", "Naromoru/Kiamathaga", "Mweiga"],
                "constituencies": ["Kieni"]
            },
            "Mathira": {
                "wards": ["Magutu", "Iriaini", "Konyu", "Ruguru", "Kirimukuyu"],
                "constituencies": ["Mathira"]
            },
            "Othaya": {
                "wards": ["Mahiga", "Iria-ini", "Chinga", "Karima"],
                "constituencies": ["Othaya"]
            },
            "Mukurweini": {
                "wards": ["Gikondi", "Mukurwe-ini", "Rugi"],
                "constituencies": ["Mukurweini"]
            },
            "Nyeri Town": {
                "wards": ["Gatitu/Muruguru", "Kiganjo/Mathari", "Rware", "Ruring'u", "Kamakwa/Mukaro"],
                "constituencies": ["Nyeri Town"]
            }
        }
    },
    
    "Kirinyaga": {
        "sub_counties": {
            "Mwea": {
                "wards": ["Wamumu", "Nyangati", "Murinduko", "Gathigiriri", "Tebere"],
                "constituencies": ["Mwea"]
            },
            "Gichugu": {
                "wards": ["Ngariama", "Kabare", "Baragwi", "Njukiini"],
                "constituencies": ["Gichugu"]
            },
            "Ndia": {
                "wards": ["Mutithi", "Ragati", "Kiine", "Karumandi"],
                "constituencies": ["Ndia"]
            },
            "Kirinyaga Central": {
                "wards": ["Kerugoya/Kutus", "Nyangati", "Mutira", "Karumandi", "Wanguru"],
                "constituencies": ["Kirinyaga Central"]
            }
        }
    },
    
    "Murang'a": {
        "sub_counties": {
            "Gatanga": {
                "wards": ["Kariara", "Ithanga", "Kakuzi/Mitubiri", "Mugumo-ini", "Kihumbu-ini"],
                "constituencies": ["Gatanga"]
            },
            "Kigumo": {
                "wards": ["Kinyona", "Kigumo", "Kahumbu", "Kangari", "Muthithi"],
                "constituencies": ["Kigumo"]
            },
            "Kangema": {
                "wards": ["Muguru", "Kanyenya-ini", "Gaichanjiru", "Rwathia"],
                "constituencies": ["Kangema"]
            },
            "Mathioya": {
                "wards": ["Kiru", "Kamacharia", "Muguru", "Gitugi"],
                "constituencies": ["Mathioya"]
            },
            "Kandara": {
                "wards": ["Ng'araria", "Muruka", "Kagundu-ini", "Ithiru", "Ruchu"],
                "constituencies": ["Kandara"]
            },
            "Kahuro": {
                "wards": ["Gaturi", "Wangu", "Nginda", "Mugoiri"],
                "constituencies": ["Kahuro"]
            },
            "Kiharu": {
                "wards": ["Wangu", "Mugoiri", "Mbiri", "Township", "Murarandia"],
                "constituencies": ["Kiharu"]
            },
            "Maragwa": {
                "wards": ["Makuyu", "Kambiti", "Kamahuha", "Ichagaki", "Kimorori/Wempa"],
                "constituencies": ["Maragwa"]
            }
        }
    },
    
    "Kiambu": {
        "sub_counties": {
            "Gatundu South": {
                "wards": ["Kiamwangi", "Kiganjo", "Ndarugu", "Ngenda"],
                "constituencies": ["Gatundu South"]
            },
            "Gatundu North": {
                "wards": ["Githobokoni", "Chania", "Mang'u"],
                "constituencies": ["Gatundu North"]
            },
            "Juja": {
                "wards": ["Murera", "Theta", "Juja", "Witeithie", "Kalimoni"],
                "constituencies": ["Juja"]
            },
            "Thika Town": {
                "wards": ["Township", "Kamenu", "Hospital", "Gatuanyaga", "Ngoliba"],
                "constituencies": ["Thika Town"]
            },
            "Ruiru": {
                "wards": ["Biashara", "Gatongora", "Kahawa Sukari", "Kahawa Wendani", "Kiuu", "Mwiki", "Mwihoko"],
                "constituencies": ["Ruiru"]
            },
            "Githunguri": {
                "wards": ["Githunguri", "Githiga", "Ikinu", "Ngewa", "Komothai"],
                "constituencies": ["Githunguri"]
            },
            "Kiambu": {
                "wards": ["Township", "Ndumberi", "Riabai", "Ting'ang'a"],
                "constituencies": ["Kiambu"]
            },
            "Kiambaa": {
                "wards": ["Cianda", "Karuri", "Ndenderu", "Muchatha", "Kihara"],
                "constituencies": ["Kiambaa"]
            },
            "Kabete": {
                "wards": ["Gitaru", "Muguga", "Nyadhuna", "Kabete", "Uthiru"],
                "constituencies": ["Kabete"]
            },
            "Kikuyu": {
                "wards": ["Karai", "Nachu", "Sigona", "Kikuyu", "Kinoo"],
                "constituencies": ["Kikuyu"]
            },
            "Limuru": {
                "wards": ["Bibirioni", "Limuru Central", "Ndeiya", "Limuru East", "Ngecha Tigoni"],
                "constituencies": ["Limuru"]
            },
            "Lari": {
                "wards": ["Kinale", "Kijabe", "Nyanduma", "Kamburu", "Lari/Kirenga"],
                "constituencies": ["Lari"]
            }
        }
    },
    
    "Turkana": {
        "sub_counties": {
            "Turkana North": {
                "wards": ["Kaeris", "Lake Zone", "Lapur", "Kibish"],
                "constituencies": ["Turkana North"]
            },
            "Turkana West": {
                "wards": ["Kakuma", "Lopur", "Letea", "Songot", "Kalobeyei"],
                "constituencies": ["Turkana West"]
            },
            "Turkana Central": {
                "wards": ["Kerio Delta", "Kang'atotha", "Kalokol", "Lodwar Township", "Kanamkemer"],
                "constituencies": ["Turkana Central"]
            },
            "Loima": {
                "wards": ["Kotaruk/Lobei", "Turkwel", "Loima", "Lokiriama/Lorengippi"],
                "constituencies": ["Loima"]
            },
            "Turkana South": {
                "wards": ["Kaputir", "Katilia", "Lobokat", "Kalapata", "Lokichar"],
                "constituencies": ["Turkana South"]
            },
            "Turkana East": {
                "wards": ["Kapedo/Napeitom", "Katilu", "Lokori/Kochodin"],
                "constituencies": ["Turkana East"]
            }
        }
    },
    
    "West Pokot": {
        "sub_counties": {
            "Kapenguria": {
                "wards": ["Riwo", "Kapenguria", "Mnagei", "Siyoi", "Endugh", "Sook"],
                "constituencies": ["Kapenguria"]
            },
            "Sigor": {
                "wards": ["Sekerr", "Masool", "Lomut", "Weiwei"],
                "constituencies": ["Sigor"]
            },
            "Kacheliba": {
                "wards": ["Suam", "Kodich", "Kasei", "Kapchok", "Kiwawa"],
                "constituencies": ["Kacheliba"]
            },
            "Pokot South": {
                "wards": ["Chepareria", "Batei", "Lelan", "Tapach"],
                "constituencies": ["Pokot South"]
            }
        }
    },
    
    "Samburu": {
        "sub_counties": {
            "Samburu West": {
                "wards": ["Lodokejek", "Suguta Marmar", "Maralal", "Loosuk", "Poro"],
                "constituencies": ["Samburu West"]
            },
            "Samburu North": {
                "wards": ["El-barta", "Nachola", "Ndoto", "Ngutuk Ongiron", "Baawa"],
                "constituencies": ["Samburu North"]
            },
            "Samburu East": {
                "wards": ["Waso", "Wamba West", "Wamba East", "Wamba North"],
                "constituencies": ["Samburu East"]
            }
        }
    },
    
    "Trans Nzoia": {
        "sub_counties": {
            "Kwanza": {
                "wards": ["Kapomboi", "Kwanza", "Keiyo", "Bidii"],
                "constituencies": ["Kwanza"]
            },
            "Endebess": {
                "wards": ["Chepchoina", "Endebess", "Matumbei"],
                "constituencies": ["Endebess"]
            },
            "Saboti": {
                "wards": ["Tuwani", "Saboti", "Machewa", "Kinyoro", "Matisi"],
                "constituencies": ["Saboti"]
            },
            "Kiminini": {
                "wards": ["Kiminini", "Waitaluk", "Sirende", "Sikhendu", "Nabiswa"],
                "constituencies": ["Kiminini"]
            },
            "Cherangany": {
                "wards": ["Sinyerere", "Makutano", "Kaplamai", "Motosiet", "Cherangany/Suwerwa", "Chepsiro/Kiptoror", "Sitatunga"],
                "constituencies": ["Cherangany"]
            }
        }
    },
    
    "Uasin Gishu": {
        "sub_counties": {
            "Soy": {
                "wards": ["Segero/Barsombe", "Kipsomba", "Soy", "Kuinet/Kapsuswa", "Kapkures", "Ziwa", "Mois Bridge"],
                "constituencies": ["Soy"]
            },
            "Turbo": {
                "wards": ["Huruma", "Ngenyilel", "Tapsagoi", "Kamagut", "Kapsoya", "Kimumu", "Kiplombe"],
                "constituencies": ["Turbo"]
            },
            "Moiben": {
                "wards": ["Tembelio", "Sergoit", "Karuna/Meibeki", "Moiben", "Kimumu"],
                "constituencies": ["Moiben"]
            },
            "Ainabkoi": {
                "wards": ["Kapsoya", "Kaptagat", "Ainabkoi/Olare"],
                "constituencies": ["Ainabkoi"]
            },
            "Kapseret": {
                "wards": ["Simat/Kapseret", "Kipkenyo", "Ngeria", "Megun", "Langas"],
                "constituencies": ["Kapseret"]
            },
            "Kesses": {
                "wards": ["Racecourse", "Cheptiret/Kipchamo", "Tulwet/Chuiyat", "Tarakwa"],
                "constituencies": ["Kesses"]
            }
        }
    },
    
    "Elgeyo Marakwet": {
        "sub_counties": {
            "Marakwet East": {
                "wards": ["Kapyego", "Sambirir", "Endo", "Embobut/Embulot"],
                "constituencies": ["Marakwet East"]
            },
            "Marakwet West": {
                "wards": ["Lelan", "Sengwer", "Cherang'any/Chebororwa", "Moiben/Kuserwo", "Arror"],
                "constituencies": ["Marakwet West"]
            },
            "Keiyo North": {
                "wards": ["Emsoo", "Kamariny", "Kapchemutwa", "Tambach"],
                "constituencies": ["Keiyo North"]
            },
            "Keiyo South": {
                "wards": ["Kabiemit", "Metkei", "Soy North", "Soy South", "Chepkorio"],
                "constituencies": ["Keiyo South"]
            }
        }
    },
    
    "Nandi": {
        "sub_counties": {
            "Tinderet": {
                "wards": ["Tinderet", "Chemelil", "Songhor/Soba", "Chepkumia"],
                "constituencies": ["Tinderet"]
            },
            "Aldai": {
                "wards": ["Kabisaga", "Ndalat", "Kemeloi/Maraba", "Kobujoi", "Terik"],
                "constituencies": ["Aldai"]
            },
            "Nandi Hills": {
                "wards": ["Nandi Hills", "Chepkunyuk", "Ol'lessos", "Kapchorua"],
                "constituencies": ["Nandi Hills"]
            },
            "Chesumei": {
                "wards": ["Kaptumo/Kaboi", "Kiptuya", "Kosirai", "Lelmokwo/Ngechek", "Chemundu/Kapng'etuny"],
                "constituencies": ["Chesumei"]
            },
            "Emgwen": {
                "wards": ["Chepkumia", "Kaptel/Kamoiywo", "Kapsabet", "Kilibwoni"],
                "constituencies": ["Emgwen"]
            },
            "Mosop": {
                "wards": ["Kabwareng", "Terik", "Kabiyet", "Ndalat", "Chepterwai", "Kipkaren"],
                "constituencies": ["Mosop"]
            }
        }
    },
    
    "Baringo": {
        "sub_counties": {
            "Tiaty": {
                "wards": ["Tirioko", "Kolowa", "Ribkwo", "Silale", "Loiyamorock", "Tangulbei/Korossi"],
                "constituencies": ["Tiaty"]
            },
            "Baringo North": {
                "wards": ["Barwessa", "Kabartonjo", "Saimo/Kipsaraman", "Saimo/Soi", "Bartabwa"],
                "constituencies": ["Baringo North"]
            },
            "Baringo Central": {
                "wards": ["Kabarnet", "Sacho", "Tenges", "Ewalel/Chapchap", "Kapropita"],
                "constituencies": ["Baringo Central"]
            },
            "Baringo South": {
                "wards": ["Marigat", "Ilchamus", "Mochongoi", "Mukutani"],
                "constituencies": ["Baringo South"]
            },
            "Mogotio": {
                "wards": ["Mogotio", "Emining", "Kisanana"],
                "constituencies": ["Mogotio"]
            },
            "Eldama Ravine": {
                "wards": ["Lembus", "Lembus Kwen", "Ravine", "Koibatek"],
                "constituencies": ["Eldama Ravine"]
            }
        }
    },
    
    "Laikipia": {
        "sub_counties": {
            "Laikipia West": {
                "wards": ["Rumuruti Township", "Marmanet", "Igwamiti", "Githiga", "Salama"],
                "constituencies": ["Laikipia West"]
            },
            "Laikipia East": {
                "wards": ["Nanyuki", "Tigithi", "Thingithu", "Ngobit", "Umande"],
                "constituencies": ["Laikipia East"]
            },
            "Laikipia North": {
                "wards": ["Sosian", "Segera", "Mugogodo West", "Mugogodo East"],
                "constituencies": ["Laikipia North"]
            }
        }
    },
    
    "Nakuru": {
        "sub_counties": {
            "Molo": {
                "wards": ["Molo", "Elburgon", "Turi", "Mariashoni"],
                "constituencies": ["Molo"]
            },
            "Njoro": {
                "wards": ["Mauche", "Mau Narok", "Kihingo", "Nessuit", "Lare", "Njoro"],
                "constituencies": ["Njoro"]
            },
            "Naivasha": {
                "wards": ["Biashara", "Hell's Gate", "Lake View", "Mai Mahiu", "Naivasha East", "Viwandani"],
                "constituencies": ["Naivasha"]
            },
            "Gilgil": {
                "wards": ["Gilgil", "Elementaita", "Mbaruk/Eburu", "Malewa West", "Murindati"],
                "constituencies": ["Gilgil"]
            },
            "Kuresoi South": {
                "wards": ["Amalo", "Keringet", "Kiptagich", "Tinet"],
                "constituencies": ["Kuresoi South"]
            },
            "Kuresoi North": {
                "wards": ["Kiptororo", "Nyota", "Sirikwa", "Kamara"],
                "constituencies": ["Kuresoi North"]
            },
            "Subukia": {
                "wards": ["Subukia", "Waseges", "Kabazi"],
                "constituencies": ["Subukia"]
            },
            "Rongai": {
                "wards": ["Menengai", "Soin", "Visoi", "Mosop", "Solai"],
                "constituencies": ["Rongai"]
            },
            "Bahati": {
                "wards": ["Dundori", "Kabatini", "Kiamaina", "Lanet/Umoja", "Bahati"],
                "constituencies": ["Bahati"]
            },
            "Nakuru Town West": {
                "wards": ["Barut", "London", "Kaptembwo", "Kapkures", "Rhoda"],
                "constituencies": ["Nakuru Town West"]
            },
            "Nakuru Town East": {
                "wards": ["Biashara", "Kivumbini", "Flamingo", "Menengai West", "Nakuru East"],
                "constituencies": ["Nakuru Town East"]
            }
        }
    },
    
    "Narok": {
        "sub_counties": {
            "Kilgoris": {
                "wards": ["Kilgoris Central", "Keyian", "Angata Barikoi", "Shankoe", "Kimintet", "Lolgorian"],
                "constituencies": ["Kilgoris"]
            },
            "Emurua Dikirr": {
                "wards": ["Ilkerin", "Ololmasani", "Mogondo", "Kapsasian"],
                "constituencies": ["Emurua Dikirr"]
            },
            "Narok North": {
                "wards": ["Olokurto", "Narok Town", "Nkareta", "Olorropil", "Melili"],
                "constituencies": ["Narok North"]
            },
            "Narok East": {
                "wards": ["Mosiro", "Ildamat", "Keekonyokie", "Suswa"],
                "constituencies": ["Narok East"]
            },
            "Narok South": {
                "wards": ["Mara", "Siana", "Naikarra", "Melelo"],
                "constituencies": ["Narok South"]
            },
            "Narok West": {
                "wards": ["Ilmotiok", "Melili", "Loita", "Sogoo", "Sagamian"],
                "constituencies": ["Narok West"]
            }
        }
    },
    
    "Kajiado": {
        "sub_counties": {
            "Kajiado North": {
                "wards": ["Olkeri", "Ongata Rongai", "Nkaimurunya", "Oloolua", "Ngong"],
                "constituencies": ["Kajiado North"]
            },
            "Kajiado Central": {
                "wards": ["Purko", "Ildamat", "Dalalekutuk", "Matapato North", "Matapato South"],
                "constituencies": ["Kajiado Central"]
            },
            "Kajiado East": {
                "wards": ["Kaputiei North", "Kitengela", "Oloosirkon/Sholinke", "Kenyawa-Poka", "Imaroro"],
                "constituencies": ["Kajiado East"]
            },
            "Kajiado West": {
                "wards": ["Keekonyokie", "Iloodokilani", "Magadi", "Ewuaso Oonkidong'i", "Mosiro"],
                "constituencies": ["Kajiado West"]
            },
            "Kajiado South": {
                "wards": ["Entonet/Lenkism", "Mbirikani/Eselenkei", "Kuku", "Rombo", "Kimana"],
                "constituencies": ["Kajiado South"]
            }
        }
    },
    
    "Kericho": {
        "sub_counties": {
            "Kipkelion East": {
                "wards": ["Waldai", "Kamasian", "Chepseon", "Tendeno/Sorget"],
                "constituencies": ["Kipkelion East"]
            },
            "Kipkelion West": {
                "wards": ["Kunyak", "Kabianga", "Chilchila", "Kipkelion"],
                "constituencies": ["Kipkelion West"]
            },
            "Ainamoi": {
                "wards": ["Kapsoit", "Ainamoi", "Kapkugerwet", "Kipchebor", "Kipchimchim", "Kapsuser"],
                "constituencies": ["Ainamoi"]
            },
            "Bureti": {
                "wards": ["Kisiara", "Tebesonik", "Cheboin", "Chemosot", "Litein", "Cheplanget"],
                "constituencies": ["Bureti"]
            },
            "Belgut": {
                "wards": ["Waldai", "Kabianga", "Cheptororiet/Seretut", "Chaik", "Kapsuser"],
                "constituencies": ["Belgut"]
            },
            "Sigowet/Soin": {
                "wards": ["Sigowet", "Kaplelartet", "Soliat", "Soin"],
                "constituencies": ["Sigowet/Soin"]
            }
        }
    },
    
    "Bomet": {
        "sub_counties": {
            "Sotik": {
                "wards": ["Ndanai/Abosi", "Chemagel", "Kipsonoi", "Kapletundo", "Rongena/Manaret"],
                "constituencies": ["Sotik"]
            },
            "Chepalungu": {
                "wards": ["Kong'asis", "Nyangores", "Sigor", "Chebunyo", "Siongiroi"],
                "constituencies": ["Chepalungu"]
            },
            "Bomet East": {
                "wards": ["Merigi", "Kembu", "Longisa", "Kipreres", "Chemaner"],
                "constituencies": ["Bomet East"]
            },
            "Bomet Central": {
                "wards": ["Silibwet Township", "Ndaraweta", "Singorwet", "Chesoen", "Mutarakwa"],
                "constituencies": ["Bomet Central"]
            },
            "Konoin": {
                "wards": ["Kimulot", "Mogogosiek", "Boito", "Embomos", "Chepchabas"],
                "constituencies": ["Konoin"]
            }
        }
    },
    
    "Kakamega": {
        "sub_counties": {
            "Lugari": {
                "wards": ["Mautuma", "Lugari", "Lumakanda", "Chekalini", "Chevaywa", "Lwandeti"],
                "constituencies": ["Lugari"]
            },
            "Likuyani": {
                "wards": ["Likuyani", "Sango", "Kongoni", "Nzoia", "Sinoko"],
                "constituencies": ["Likuyani"]
            },
            "Malava": {
                "wards": ["West Kabras", "Chemuche", "East Kabras", "Butali/Chegulo", "Manda Shivanga", "Shirugu/Mugai", "South Kabras"],
                "constituencies": ["Malava"]
            },
            "Lurambi": {
                "wards": ["Butsotso East", "Butsotso South", "Butsotso Central", "Sheywe", "Mahiakalo", "Shirere"],
                "constituencies": ["Lurambi"]
            },
            "Navakholo": {
                "wards": ["Ingostse/Mathia", "Shinoyi/Shikomari/Esumeyia", "Bunyala West", "Bunyala East", "Bunyala Central"],
                "constituencies": ["Navakholo"]
            },
            "Mumias West": {
                "wards": ["Mumias Central", "Mumias North", "Etenje", "Musanda", "Malaha/Isongo/Makunga", "Ekero/Khalayi"],
                "constituencies": ["Mumias West"]
            },
            "Mumias East": {
                "wards": ["Lusheya/Lubinu", "East Wanga", "Malaha Central", "West Wanga"],
                "constituencies": ["Mumias East"]
            },
            "Matungu": {
                "wards": ["Koyonzo", "Kholera", "Khalaba", "Mayoni", "Namamali"],
                "constituencies": ["Matungu"]
            },
            "Butere": {
                "wards": ["Marama West", "Marama Central", "Marenyo-Shianda", "Marama North", "Marama South"],
                "constituencies": ["Butere"]
            },
            "Khwisero": {
                "wards": ["Kisa North", "Kisa East", "Kisa West", "Kisa Central"],
                "constituencies": ["Khwisero"]
            },
            "Shinyalu": {
                "wards": ["Isukha North", "Murhanda", "Isukha Central", "Isukha South", "Isukha East", "Isukha West"],
                "constituencies": ["Shinyalu"]
            },
            "Ikolomani": {
                "wards": ["Idakho South", "Idakho East", "Idakho North", "Idakho Central"],
                "constituencies": ["Ikolomani"]
            }
        }
    },
    
    "Vihiga": {
        "sub_counties": {
            "Vihiga": {
                "wards": ["Luanda Township", "Luanda South", "Emabungo", "Central Maragoli"],
                "constituencies": ["Vihiga"]
            },
            "Sabatia": {
                "wards": ["Busali", "Lyaduywa/Izava", "West Sabatia", "Chavakali", "North Maragoli", "Wodanga"],
                "constituencies": ["Sabatia"]
            },
            "Hamisi": {
                "wards": ["Shiru", "Muhudu", "Banja", "Tambua", "Jepkoyai"],
                "constituencies": ["Hamisi"]
            },
            "Luanda": {
                "wards": ["Luanda Township", "Wemilabi", "Mwibona", "Luanda South", "Emabungo"],
                "constituencies": ["Luanda"]
            },
            "Emuhaya": {
                "wards": ["North East Bunyore", "Central Bunyore", "West Bunyore"],
                "constituencies": ["Emuhaya"]
            }
        }
    },
    
    "Bungoma": {
        "sub_counties": {
            "Mt Elgon": {
                "wards": ["Kaptama", "Cheptais", "Chesikaki", "Chepyuk"],
                "constituencies": ["Mt Elgon"]
            },
            "Sirisia": {
                "wards": ["Namwela", "Malakisi/South Kulisiru", "Lwandanyi", "Sirisia"],
                "constituencies": ["Sirisia"]
            },
            "Kabuchai": {
                "wards": ["Kabuchai/Chwele", "West Nalondo", "Bwake/Luuya", "Mukuyuni"],
                "constituencies": ["Kabuchai"]
            },
            "Bumula": {
                "wards": ["Bumula", "Khasoko", "Kabula", "Kimaeti", "South Bukusu", "Siboti"],
                "constituencies": ["Bumula"]
            },
            "Kanduyi": {
                "wards": ["Bukembe West", "Bukembe East", "Township", "Khalaba", "Musikoma", "East Sang'alo", "Marakaru/Tuuti"],
                "constituencies": ["Kanduyi"]
            },
            "Webuye East": {
                "wards": ["Ndivisi", "Maraka", "Mihuu", "Ndalu/Tabani"],
                "constituencies": ["Webuye East"]
            },
            "Webuye West": {
                "wards": ["Misikhu", "Sitikho", "Bokoli", "Matulo"],
                "constituencies": ["Webuye West"]
            },
            "Kimilili": {
                "wards": ["Kimilili", "Maeni", "Kamukuywa", "Kibingei"],
                "constituencies": ["Kimilili"]
            },
            "Tongaren": {
                "wards": ["Mbakalo", "Naitiri/Kabuyefwe", "Milima", "Ndalu/Tabani", "Tongaren", "Soysambu/Mitua"],
                "constituencies": ["Tongaren"]
            }
        }
    },
    
    "Busia": {
        "sub_counties": {
            "Teso North": {
                "wards": ["Malaba North", "Malaba South", "Ang'urai North", "Ang'urai South", "Ang'urai East"],
                "constituencies": ["Teso North"]
            },
            "Teso South": {
                "wards": ["Ang'orom", "Chakol South", "Chakol North", "Amukura West", "Amukura East"],
                "constituencies": ["Teso South"]
            },
            "Nambale": {
                "wards": ["Nambale Township", "Bukhayo North/Walatsi", "Bukhayo East", "Bukhayo Central"],
                "constituencies": ["Nambale"]
            },
            "Matayos": {
                "wards": ["Burumba", "Marachi West", "Marachi Central", "Marachi East", "Marachi North", "Elugulu"],
                "constituencies": ["Matayos"]
            },
            "Butula": {
                "wards": ["Marachi Central", "Kingandole", "Marachi East", "Marachi North", "Marachi West"],
                "constituencies": ["Butula"]
            },
            "Funyula": {
                "wards": ["Namboboto Nambuku", "Ageng'a Nanguba", "Bwiri", "Nambale"],
                "constituencies": ["Funyula"]
            },
            "Budalangi": {
                "wards": ["Bunyala Central", "Bunyala West", "Bunyala North", "Bunyala South"],
                "constituencies": ["Budalangi"]
            }
        }
    },
    
    "Siaya": {
        "sub_counties": {
            "Ugenya": {
                "wards": ["Sidindi", "Sigomre", "Ugunja", "Ukwala", "North Ugenya", "West Ugenya", "East Ugenya"],
                "constituencies": ["Ugenya"]
            },
            "Ugunja": {
                "wards": ["Sidindi", "Sigomre", "Ugunja"],
                "constituencies": ["Ugunja"]
            },
            "Alego Usonga": {
                "wards": ["Usonga", "West Alego", "Central Alego", "Siaya Township", "North Alego", "South East Alego"],
                "constituencies": ["Alego Usonga"]
            },
            "Gem": {
                "wards": ["North Gem", "West Gem", "Central Gem", "Yala Township", "East Gem", "South Gem"],
                "constituencies": ["Gem"]
            },
            "Bondo": {
                "wards": ["West Yimbo", "Central Sakwa", "South Sakwa", "Yimbo East", "West Sakwa", "North Sakwa"],
                "constituencies": ["Bondo"]
            },
            "Rarieda": {
                "wards": ["East Asembo", "West Asembo", "North Uyoma", "South Uyoma", "West Uyoma"],
                "constituencies": ["Rarieda"]
            }
        }
    },
    
    "Kisumu": {
        "sub_counties": {
            "Kisumu East": {
                "wards": ["Kajulu", "Kolwa East", "Manyatta B", "Nyalenda A"],
                "constituencies": ["Kisumu East"]
            },
            "Kisumu West": {
                "wards": ["North West Kisumu", "Central Kisumu", "Kisumu North", "West Kisumu", "South West Kisumu"],
                "constituencies": ["Kisumu West"]
            },
            "Kisumu Central": {
                "wards": ["Railways", "Migosi", "Shaurimoyo Kaloleni", "Market Milimani", "Kondele", "Nyalenda B"],
                "constituencies": ["Kisumu Central"]
            },
            "Seme": {
                "wards": ["West Seme", "Central Seme", "East Seme", "North Seme"],
                "constituencies": ["Seme"]
            },
            "Nyando": {
                "wards": ["West Kano", "South West Nyakach", "North Nyakach", "Central Nyakach", "Awasi/Onjiko", "Ahero", "Kabonyo/Kanyagwal"],
                "constituencies": ["Nyando"]
            },
            "Muhoroni": {
                "wards": ["Miwani", "Ombeyi", "Masogo/Nyang'oma", "Chemelil", "Muhoroni/Koru"],
                "constituencies": ["Muhoroni"]
            },
            "Nyakach": {
                "wards": ["South West Nyakach", "North Nyakach", "Central Nyakach", "West Nyakach", "South East Nyakach"],
                "constituencies": ["Nyakach"]
            }
        }
    },
    
    "Homa Bay": {
        "sub_counties": {
            "Kasipul": {
                "wards": ["West Kasipul", "South Kasipul", "Central Kasipul", "East Kamagak", "West Kamagak"],
                "constituencies": ["Kasipul"]
            },
            "Kabondo Kasipul": {
                "wards": ["Kabondo East", "Kabondo West", "Kokwanyo/Kakelo", "Kojwach"],
                "constituencies": ["Kabondo Kasipul"]
            },
            "Karachuonyo": {
                "wards": ["West Karachuonyo", "North Karachuonyo", "Central Karachuonyo", "Kibiri", "Wangchieng", "Kendu Bay Town"],
                "constituencies": ["Karachuonyo"]
            },
            "Rangwe": {
                "wards": ["West Gem", "East Gem", "Kochia", "Kagan"],
                "constituencies": ["Rangwe"]
            },
            "Homa Bay Town": {
                "wards": ["Homa Bay Central", "Homa Bay Arujo", "Homa Bay West", "Homa Bay East"],
                "constituencies": ["Homa Bay Town"]
            },
            "Ndhiwa": {
                "wards": ["Kwabwai", "Kanyadoto", "Kanyamwa Kosewe", "Kanyamwa Kologi", "Kabuoch North", "Kabuoch South/Pala"],
                "constituencies": ["Ndhiwa"]
            },
            "Suba North": {
                "wards": ["Mfangano Island", "Rusinga Island", "Kasgunga", "Gembe", "Lambwe"],
                "constituencies": ["Suba North"]
            },
            "Suba South": {
                "wards": ["Gwassi South", "Gwassi North", "Kaksingri West", "Ruma Kaksingri East"],
                "constituencies": ["Suba South"]
            }
        }
    },
    
    "Migori": {
        "sub_counties": {
            "Rongo": {
                "wards": ["North Kamagambo", "Central Kamagambo", "East Kamagambo", "South Kamagambo"],
                "constituencies": ["Rongo"]
            },
            "Awendo": {
                "wards": ["North Sakwa", "South Sakwa", "West Sakwa", "Central Sakwa"],
                "constituencies": ["Awendo"]
            },
            "Suna East": {
                "wards": ["God Jope", "Suna Central", "Kakrao", "Kwa"],
                "constituencies": ["Suna East"]
            },
            "Suna West": {
                "wards": ["Wiga", "Wasweta II", "Ragana-Oruba", "Wasimbete"],
                "constituencies": ["Suna West"]
            },
            "Uriri": {
                "wards": ["West Kanyamkago", "North Kanyamkago", "Central Kanyamkago", "South Kanyamkago", "East Kanyamkago"],
                "constituencies": ["Uriri"]
            },
            "Nyatike": {
                "wards": ["Karungu", "Kaler", "Got Kachola", "Kanyasa", "North Kadem", "Macalder/Kanyarwanda"],
                "constituencies": ["Nyatike"]
            },
            "Kuria West": {
                "wards": ["Bukira East", "Bukira Central/Ikerege", "Isibania", "Makerero", "Masaba", "Tagare", "Nyamosense/Komosoko"],
                "constituencies": ["Kuria West"]
            },
            "Kuria East": {
                "wards": ["Kegonga", "Ntimaru West", "Ntimaru East", "Nyabasi East", "Nyabasi West"],
                "constituencies": ["Kuria East"]
            }
        }
    },
    
    "Kisii": {
        "sub_counties": {
            "Kitutu Chache North": {
                "wards": ["Monyerero", "Sensi", "Marani", "Kegogi"],
                "constituencies": ["Kitutu Chache North"]
            },
            "Kitutu Chache South": {
                "wards": ["Bogusero", "Bogeka", "Nyakoe", "Kitutu Central", "Nyatieko"],
                "constituencies": ["Kitutu Chache South"]
            },
            "Nyaribari Masaba": {
                "wards": ["Ichuni", "Nyamasibi", "Masimba", "Gesusu", "Kiamokama"],
                "constituencies": ["Nyaribari Masaba"]
            },
            "Nyaribari Chache": {
                "wards": ["Bobaracho", "Kisii Central", "Keumbu", "Kiogoro", "Birongo", "Ibeno"],
                "constituencies": ["Nyaribari Chache"]
            },
            "Bobasi": {
                "wards": ["Masige West", "Masige East", "Basi Central", "Nyacheki", "Bassi Bogetaorio", "Bobasi Boitangare"],
                "constituencies": ["Bobasi"]
            },
            "Bomachoge Borabu": {
                "wards": ["Bomariba", "Bogiakumu", "Bomorenda", "Riana"],
                "constituencies": ["Bomachoge Borabu"]
            },
            "Bomachoge Chache": {
                "wards": ["Majoge Basi", "Boochi/Tendere", "Bosoti/Sengera"],
                "constituencies": ["Bomachoge Chache"]
            },
            "South Mugirango": {
                "wards": ["Tabaka", "Boikanga", "Bogetenga", "Borabu/Chitago", "Moticho", "Getenga"],
                "constituencies": ["South Mugirango"]
            },
            "Bonchari": {
                "wards": ["Bomariba", "Bogiakumu", "Bomorenda", "Riana"],
                "constituencies": ["Bonchari"]
            }
        }
    },
    
    "Nyamira": {
        "sub_counties": {
            "Kitutu Masaba": {
                "wards": ["Rigoma", "Gachuba", "Kemera", "Magombo", "Manga", "Gesima"],
                "constituencies": ["Kitutu Masaba"]
            },
            "West Mugirango": {
                "wards": ["Bogichora", "Bosamaro", "Bonyamatuta", "Township"],
                "constituencies": ["West Mugirango"]
            },
            "North Mugirango": {
                "wards": ["Itibo", "Bomwagamo", "Bokeira", "Magwagwa", "Ekerenyo"],
                "constituencies": ["North Mugirango"]
            },
            "Borabu": {
                "wards": ["Mekenene", "Kiabonyoru", "Nyansiongo", "Esise", "Mikei"],
                "constituencies": ["Borabu"]
            }
        }
    },
    
    "Nairobi": {
        "sub_counties": {
            "Westlands": {
                "wards": ["Kitisuru", "Parklands/Highridge", "Karura", "Kangemi", "Mountain View"],
                "constituencies": ["Westlands"]
            },
            "Dagoretti North": {
                "wards": ["Kilimani", "Kawangware", "Gatina", "Kileleshwa", "Kabiro"],
                "constituencies": ["Dagoretti North"]
            },
            "Dagoretti South": {
                "wards": ["Mutuini", "Ngando", "Riruta", "Uthiru/Ruthimitu", "Waithaka"],
                "constituencies": ["Dagoretti South"]
            },
            "Langata": {
                "wards": ["Karen", "Nairobi West", "Mugumo-ini", "South C", "Nyayo Highrise"],
                "constituencies": ["Langata"]
            },
            "Kibra": {
                "wards": ["Laini Saba", "Lindi", "Makina", "Woodley/Kenyatta Golf Course", "Sarang'ombe"],
                "constituencies": ["Kibra"]
            },
            "Roysambu": {
                "wards": ["Githurai", "Kahawa West", "Zimmerman", "Roysambu", "Kahawa"],
                "constituencies": ["Roysambu"]
            },
            "Kasarani": {
                "wards": ["Clay City", "Mwiki", "Kasarani", "Njiru", "Ruai"],
                "constituencies": ["Kasarani"]
            },
            "Ruaraka": {
                "wards": ["Baba Dogo", "Utalii", "Mathare North", "Lucky Summer", "Korogocho"],
                "constituencies": ["Ruaraka"]
            },
            "Embakasi South": {
                "wards": ["Imara Daima", "Kwa Njenga", "Kwa Reuben", "Pipeline", "Kware"],
                "constituencies": ["Embakasi South"]
            },
            "Embakasi North": {
                "wards": ["Kariobangi North", "Dandora Area I", "Dandora Area II", "Dandora Area III", "Dandora Area IV"],
                "constituencies": ["Embakasi North"]
            },
            "Embakasi Central": {
                "wards": ["Kayole North", "Kayole Central", "Kayole South", "Komarock", "Matopeni/Spring Valley"],
                "constituencies": ["Embakasi Central"]
            },
            "Embakasi East": {
                "wards": ["Upper Savannah", "Lower Savannah", "Embakasi", "Utawala", "Mihango"],
                "constituencies": ["Embakasi East"]
            },
            "Embakasi West": {
                "wards": ["Umoja I", "Umoja II", "Mowlem", "Kariobangi South"],
                "constituencies": ["Embakasi West"]
            },
            "Makadara": {
                "wards": ["Maringo/Hamza", "Viwandani", "Harambee", "Makongeni"],
                "constituencies": ["Makadara"]
            },
            "Kamukunji": {
                "wards": ["Pumwani", "Eastleigh North", "Eastleigh South", "Airbase", "California"],
                "constituencies": ["Kamukunji"]
            },
            "Starehe": {
                "wards": ["Nairobi Central", "Ngara", "Pangani", "Ziwani/Kariokor", "Landimawe", "Nairobi South"],
                "constituencies": ["Starehe"]
            },
            "Mathare": {
                "wards": ["Hospital", "Mabatini", "Huruma", "Ngei", "Mlango Kubwa", "Kiamaiko"],
                "constituencies": ["Mathare"]
            }
        }
    }
}


def get_all_counties():
    """Get list of all 47 counties"""
    return sorted(list(KENYA_LOCATIONS.keys()))


def get_sub_counties(county):
    """Get sub-counties for a specific county"""
    if county not in KENYA_LOCATIONS:
        return []
    return sorted(list(KENYA_LOCATIONS[county]["sub_counties"].keys()))


def get_wards(county, sub_county):
    """Get wards for a specific sub-county"""
    if county not in KENYA_LOCATIONS:
        return []
    if sub_county not in KENYA_LOCATIONS[county]["sub_counties"]:
        return []
    return sorted(KENYA_LOCATIONS[county]["sub_counties"][sub_county]["wards"])


def get_constituencies(county, sub_county=None):
    """Get constituencies for a county or sub-county"""
    if county not in KENYA_LOCATIONS:
        return []
    
    if sub_county:
        if sub_county not in KENYA_LOCATIONS[county]["sub_counties"]:
            return []
        return KENYA_LOCATIONS[county]["sub_counties"][sub_county]["constituencies"]
    
    # Get all constituencies for the county
    constituencies = []
    for sc_data in KENYA_LOCATIONS[county]["sub_counties"].values():
        constituencies.extend(sc_data["constituencies"])
    return sorted(list(set(constituencies)))


def search_locations(query, limit=50):
    """Search across all location levels"""
    query_lower = query.lower()
    results = []
    
    for county, county_data in KENYA_LOCATIONS.items():
        # Search county
        if query_lower in county.lower():
            results.append({
                "type": "county",
                "county": county,
                "display": f"{county} County"
            })
        
        # Search sub-counties, wards, and constituencies
        for sub_county, sc_data in county_data["sub_counties"].items():
            if query_lower in sub_county.lower():
                results.append({
                    "type": "sub_county",
                    "county": county,
                    "sub_county": sub_county,
                    "display": f"{sub_county} ({county})"
                })
            
            # Search wards
            for ward in sc_data["wards"]:
                if query_lower in ward.lower():
                    results.append({
                        "type": "ward",
                        "county": county,
                        "sub_county": sub_county,
                        "ward": ward,
                        "display": f"{ward} Ward ({sub_county}, {county})"
                    })
            
            # Search constituencies
            for constituency in sc_data["constituencies"]:
                if query_lower in constituency.lower():
                    results.append({
                        "type": "constituency",
                        "county": county,
                        "sub_county": sub_county,
                        "constituency": constituency,
                        "display": f"{constituency} Constituency ({county})"
                    })
    
    return results[:limit]


# Stats
TOTAL_COUNTIES = len(KENYA_LOCATIONS)
TOTAL_SUB_COUNTIES = sum(len(county_data["sub_counties"]) for county_data in KENYA_LOCATIONS.values())
TOTAL_WARDS = sum(
    len(sc_data["wards"]) 
    for county_data in KENYA_LOCATIONS.values() 
    for sc_data in county_data["sub_counties"].values()
)
TOTAL_CONSTITUENCIES = sum(
    len(set(sc_data["constituencies"]))
    for county_data in KENYA_LOCATIONS.values() 
    for sc_data in county_data["sub_counties"].values()
)
