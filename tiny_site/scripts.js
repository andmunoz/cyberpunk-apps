// Base Config Values
const SERVERAPI = "https://cyberpunk-database.firebaseio.com/";

// General Functions
function toggleVisibility(showId, hideId1, hideId2) {
    $(hideId1).hide();
    if (hideId2) $(hideId2).hide();
    $(showId).show();
}

// Datatable Functions
function loadData(route, title, hasData) {
    toggleVisibility("#section_spinner", "#section_data", "#section_tools");

    $("#data_title").text(title);

    if (hasData) {
        $("#data_results").DataTable().destroy();
        $("#data_results>tbody").text("")
    }

    $.ajax({  
        type: "GET",  
        url: SERVERAPI + route + ".json",    
        dataType: "json", 
        success: function (data) {  
            $.each(data, function(i, item){
                let row = "<tr>"+
                "<td class=\" d-none d-md-table-cell\">" + item.id + "</td>" + 
                "   <td><a href=\"#\" class=\"btn text-start text-wrap\" data-bs-toggle=\"modal\" data-bs-target=\"#viewItem" + item.id + "Modal\">" + item.name + "</a>" + constructModal(item) +"</td>" +
                "   <td class=\" d-none d-md-table-cell\">" + item.description + "</td>" +
                "   <td class=\"text-end\">" + item.cost + " creds</td>" +
                "   <td class=\" d-none d-md-table-cell\">" +
                "       <button class=\"btn btn-primary\" type=\"button\" data-bs-toggle=\"modal\" data-bs-target=\"#viewItem" + item.id + "Modal\"><i class=\"fa-solid fa-eye\"></i></button>" + 
                "   </td>" +
                "</tr>";						 
                $("#data_results>tbody").append(row);
            });

            $("#data_results").DataTable({
                info: true,
                ordering: true,
                paging: true,
                processing: true,
                stateSave: true,
                pageLength: 50,
                language: {
                    "retrieve": true,
                    "lengthMenu": "Mostrando _MENU_ registros por página",
                    "search": "Buscar:",
                    "zeroRecords": "No se ha encontrado nada",
                    "info": "Mostrando página _PAGE_ de _PAGES_",
                    "infoEmpty": "Mostrando 0 de 0 registros",
                    "infoFiltered": "(filtrado de un total de _MAX_ registros)", 
                    "paginate": {
                        "first":      "Primera",
                        "last":       "Última",
                        "next":       "Siguiente",
                        "previous":   "Anterior"
                    },
                    "loadingRecords": "Cargando datos..."
                }
            });

            toggleVisibility("#section_data", "#section_spinner");
        }, 
    });         
}

function constructModal(item) {
    let modalHTML = "<div class=\"modal fade\" id=\"viewItem" + item.id + "Modal\" tabindex=\"-1\" aria-labelledby=\"viewItem" + item.id + "ModalLabel\" aria-hidden=\"true\">" +
                    "    <div class=\"modal-dialog modal-lg\">" +
                    "       <div class=\"modal-content\">" +
                    "           <div class=\"modal-header\">" +
                    "               <h1 class=\"modal-title fs-5 text-wrap\" id=\"viewItem" + item.id + "ModalLabel\">" + item.name + "</h1>" +
                    "               <button type=\"button\" class=\"btn-close\" data-bs-dismiss=\"modal\" aria-label=\"Cerrar\"></button>" +
                    "           </div>" +
                    "           <div class=\"modal-body\">" +
                    "               <div class=\"mb-3\">" +
                    "                   <table class=\"table table-borderless\">" +
                    "                       <caption>&nbsp;</caption>" +
                    "                       <tbody>";
    $.each(item, function(key, value){
        if (key != "image") {
            modalHTML += "                              <tr>" +
                         "                                  <th scope=\"row\" class=\"text-end\">" + key + "</td>" +
                         "                                  <td class=\"text-wrap\">" + value + "</td>" +
                         "                              </tr>"
        }
    });
                
    modalHTML +=    "                        </tbody>" +
                    "                    </table>" +
                    "                </div>" +
                    "            </div>" +
                    "            <div class=\"modal-footer\">" +
                    "                <button type=\"button\" class=\"btn btn-secondary\" data-bs-dismiss=\"modal\">Cerrar</button>" +
                    "            </div>" +
                    "        </div>" +
                    "    </div>" +
                    "</div>";
    return modalHTML;
}

// Tools General Functions
let lifepathTables = {};

let shoppingCart = [];
let shoppingItems = 0;

let armorTables = [];
let armorRows = 0

let brawlingTables = [];
let brawlingRows = 0;

let damageTables = [];
let damageRows = 0;

function calculateMixedCP(cpLayer1, cpLayer2) {
    let diff = Math.abs(cpLayer1 - cpLayer2);
    let cpMixed = Math.max(cpLayer1, cpLayer2);
    if (diff <= 4) cpMixed += 5;
    else if (diff <= 8) cpMixed += 4; 
    else if (diff <= 14) cpMixed += 3; 
    else if (diff <= 20) cpMixed += 2; 
    else if (diff <= 26) cpMixed += 1; 
    return cpMixed;
}

function loadTools(title) {
    toggleVisibility("#section_spinner", "#section_data", "#section_tools");

    loadLifePathTables();

    armorTables = loadArmorTables();
    addArmorRow();

    brawlingTables = loadBrawlingTables();
    brawlingRows++;
    let newRow = '<tr class="brawling_form_row">' +
                '<td>' + brawlingRows + '</td>' +
                '<td><input class="form-control" id="brawling_technique_' + brawlingRows + '" value="Pelea (1)" readonly="yes"/></td>' +
                '<td><input class="form-control" type="text" id="brawling_level_' + brawlingRows + '" value="0" onchange="calculateBrawlingTecniques(' + brawlingRows + ')"/></td>' +
             '</tr>';
    $('#brawling_table>tbody').append(newRow);
    brawlingRows++;
    newRow = '<tr class="brawling_form_row">' +
                '<td>' + brawlingRows + '</td>' +
                '<td><input class="form-control" id="brawling_technique_' + brawlingRows + '" value="Esquivar (1)" readonly="yes"/></td>' +
                '<td><input class="form-control" type="text" id="brawling_level_' + brawlingRows + '" value="0" onchange="calculateBrawlingTecniques(' + brawlingRows + ')"/></td>' +
             '</tr>';
    $('#brawling_table>tbody').append(newRow);
    brawlingRows++;
    newRow = '<tr class="brawling_form_row">' +
                '<td>' + brawlingRows + '</td>' +
                '<td><input class="form-control" id="brawling_technique_' + brawlingRows + '" value="Combate Cuerpo a Cuerpo (1)" readonly="yes"/></td>' +
                '<td><input class="form-control" type="text" id="brawling_level_' + brawlingRows + '" value="0" onchange="calculateBrawlingTecniques(' + brawlingRows + ')"/></td>' +
             '</tr>';
    $('#brawling_table>tbody').append(newRow);

    damageTables = loadDamageTables();
    addDamageRow();

    toggleVisibility("#section_tools", "#section_spinner");
}

function loadLifePathTables() {
    asyncLoadLifePathComponent('Clothes', 'Style');
    asyncLoadLifePathComponent('Hair', 'Style');
    asyncLoadLifePathComponent('Traits', 'Style');
    asyncLoadLifePathComponent('Origin', 'Ethnic');

    asyncLoadLifePathComponent('Personality', 'Motivations');
    asyncLoadLifePathComponent('MostValuedPerson', 'Motivations');
    asyncLoadLifePathComponent('MostValuable', 'Motivations');
    asyncLoadLifePathComponent('MostValuedThing', 'Motivations');
    asyncLoadLifePathComponent('PeopleOpinion', 'Motivations');

    asyncLoadLifePathComponent('Class', 'Family');
    asyncLoadLifePathComponent('Parents', 'Family');
    asyncLoadLifePathComponent('ParentTragedy', 'Family');
    asyncLoadLifePathComponent('FamilySituation', 'Family');
    asyncLoadLifePathComponent('FamilyTragedy', 'Family');
    asyncLoadLifePathComponent('Childhood', 'Family');
    asyncLoadLifePathComponent('SiblingsQuantity', 'Family');
    asyncLoadLifePathComponent('SiblingGender', 'Family');
    asyncLoadLifePathComponent('SiblingOrder', 'Family');
    asyncLoadLifePathComponent('SiblingRelationship', 'Family');

    asyncLoadLifePathComponent('TypeOfEvent', 'Events');
    asyncLoadLifePathComponent('EventSuccess', 'Events');
    asyncLoadLifePathComponent('EventFailure', 'Events');
    asyncLoadLifePathComponent('EventFriend', 'Events');
    asyncLoadLifePathComponent('EventEnemy', 'Events');
    asyncLoadLifePathComponent('EventLoveDate', 'Events');

    return;
}

function asyncLoadLifePathComponent(component, parent) {
    $.ajax({  
        type: "GET",  
        url: SERVERAPI + 'Lists/Lifepath/' + parent + '/' + component + '.json',    
        dataType: "json", 
        success: function (data) {
            if (typeof lifepathTables[parent] === "undefined")
                lifepathTables[parent] = {};
            let componentMap = Object.entries(data).map(([key, value]) => ({[key]: value}));
            let values = []
            componentMap.forEach(item => {
                let id = parseInt(Object.keys(item)[0]) - 1;
                let content = Object.values(item)[0];
                values[id] = content;
            });
            lifepathTables[parent][component] = values;
        }, 
    });    
}

function loadBrawlingTables() {
    $.ajax({  
        type: "GET",  
        url: SERVERAPI + 'Lists/Martial' + ".json",    
        dataType: "json", 
        success: function (data) {
            let martialMap = Object.entries(data).map(([key, value]) => ({[key]: value}));
            brawlingTables['martials'] = [];
            martialMap.forEach(martial => {
                let martialAbility = {
                    'name': '',
                    'difficult': 0,
                    'count': 0,
                    'techniques': [
                        {'name': 'barrier', 'value': 0},
                        {'name': 'block', 'value': 0},
                        {'name': 'disarm', 'value': 0},
                        {'name': 'dodge', 'value': 0},
                        {'name': 'feint', 'value': 0},
                        {'name': 'grapple', 'value': 0},
                        {'name': 'kick', 'value': 0},
                        {'name': 'prone', 'value': 0},
                        {'name': 'punch', 'value': 0},
                        {'name': 'quarry', 'value': 0},
                        {'name': 'strangle', 'value': 0},
                        {'name': 'throw', 'value': 0},
                        {'name': 'weapon', 'value': 0}
                    ]
                };
                let martialName = Object.keys(martial)[0];
                let martialAttributes = Object.values(martial)[0];
                martialAbility['name'] = martialName;
                martialAbility['techniques'] = [];
                let attributesMap = Object.entries(martialAttributes).map(([clave, valor]) => ({[clave]: valor}));
                attributesMap.forEach(attribute => {
                    let key = Object.keys(attribute)[0];
                    let value = Object.values(attribute)[0];
                    if (key == 'difficult') martialAbility['difficult'] = value;
                    else if (key == 'techniques') martialAbility['count'] = value;
                    else martialAbility['techniques'].push({
                        'name': key,
                        'value': value
                    });
                });
                brawlingTables['martials'].push(martialAbility);
            });
        }, 
    });    
    return {
        'abilities': [
            {
                'name': 'Pelea',
                'difficult': 1,
                'count': 10,
                'techniques': [
                    {'name': 'barrier', 'value': 1},
                    {'name': 'block', 'value': 1},
                    {'name': 'disarm', 'value': 1},
                    {'name': 'dodge', 'value': 0},
                    {'name': 'feint', 'value': 1},
                    {'name': 'grapple', 'value': 1},
                    {'name': 'kick', 'value': 1},
                    {'name': 'prone', 'value': 1},
                    {'name': 'punch', 'value': 1},
                    {'name': 'quarry', 'value': 1},
                    {'name': 'strangle', 'value': 1},
                    {'name': 'throw', 'value': 1},
                    {'name': 'weapon', 'value': 0}
                ]
            }, 
            {
                'name': 'Esquivar',
                'difficult': 1,
                'count': 1,
                'techniques': [
                    {'name': 'barrier', 'value': 0},
                    {'name': 'block', 'value': 0},
                    {'name': 'disarm', 'value': 0},
                    {'name': 'dodge', 'value': 1},
                    {'name': 'feint', 'value': 0},
                    {'name': 'grapple', 'value': 0},
                    {'name': 'kick', 'value': 0},
                    {'name': 'prone', 'value': 0},
                    {'name': 'punch', 'value': 0},
                    {'name': 'quarry', 'value': 0},
                    {'name': 'strangle', 'value': 0},
                    {'name': 'throw', 'value': 0},
                    {'name': 'weapon', 'value': 0}
                ]
            }, 
            {
                'name': 'Combate Cuerpo a Cuerpo',
                'difficult': 1,
                'count': 1,
                'techniques': [
                    {'name': 'barrier', 'value': 0},
                    {'name': 'block', 'value': 0},
                    {'name': 'disarm', 'value': 0},
                    {'name': 'dodge', 'value': 0},
                    {'name': 'feint', 'value': 0},
                    {'name': 'grapple', 'value': 0},
                    {'name': 'kick', 'value': 0},
                    {'name': 'prone', 'value': 0},
                    {'name': 'punch', 'value': 0},
                    {'name': 'quarry', 'value': 0},
                    {'name': 'strangle', 'value': 0},
                    {'name': 'throw', 'value': 0},
                    {'name': 'weapon', 'value': 1}
                ]
            }    
        ]
    };
}

function loadArmorTables() {
    let armorTypes = [{'type': 'Blando', 'code': 'cpb'}, 
                      {'type': 'Duro', 'code': 'cpd'}];
    let coverage =   [{'cover': 'Cabeza', 'from': 1, 'to': 1},
                      {'cover': 'Torso', 'from': 2, 'to': 4}, 
                      {'cover': 'Brazo Izquierdo', 'from': 5, 'to': 5},
                      {'cover': 'Brazos Derecho', 'from': 6, 'to': 6},
                      {'cover': 'Brazos', 'from': 5, 'to': 6},
                      {'cover': 'Superior', 'from': 2, 'to': 6},
                      {'cover': 'Pierna Izquierda', 'from': 7, 'to': 8},
                      {'cover': 'Pierna Derecha', 'from': 9, 'to': 10},
                      {'cover': 'Piernas', 'from': 7, 'to': 10},
                      {'cover': 'Cuerpo', 'from': 2, 'to': 10}, 
                      {'cover': 'Todo', 'from': 1, 'to': 10}];
    let damageType = [{'code': 'cpn', 'CPB': 1, 'CPD': 1},
                      {'code': 'cpp', 'CPB': 1, 'CPD': 0.5}, 
                      {'code': 'cpf', 'CPB': 0.5, 'CPD': 1}, 
                      {'code': 'cpm', 'CPB': 0.666, 'CPD': 0.333}];
    return {
        'armorTypes': armorTypes,
        'coverage': coverage,
        'damageTypes': damageType
    };
}

function loadDamageTables() {
    let localizations = [{'rollFrom': 1, 'rollTo': 1, 'locale': 'Cabeza', 'factor':2, 'result':'Muerte'},
                         {'rollFrom': 2, 'rollTo': 4, 'locale': 'Torso', 'factor':1, 'result':''}, 
                         {'rollFrom': 5, 'rollTo': 5, 'locale': 'Brazo Izquierdo', 'factor':1, 'result':'Miembro Mutilado'},
                         {'rollFrom': 6, 'rollTo': 6, 'locale': 'Brazo Derecho', 'factor':1, 'result':'Miembro Mutilado'},
                         {'rollFrom': 7, 'rollTo': 8, 'locale': 'Pierna Izquierda', 'factor':1, 'result':'Miembro Mutilado'},
                         {'rollFrom': 9, 'rollTo': 10, 'locale': 'Pierna Derecha', 'factor':1, 'result':'Miembro Mutilado'}];
    let healthStatus =  [{'min': 0, 'max': 0, 'status': 'Sano', 'stun': false, 'death': false, 'penalty': 0},
                         {'min': 1, 'max': 4, 'status': 'Leve', 'stun': true, 'death': false, 'penalty': 0}, 
                         {'min': 5, 'max': 8, 'status': 'Grave', 'stun': true, 'death': false, 'penalty': -1}, 
                         {'min': 9, 'max': 12, 'status': 'Crítico', 'stun': true, 'death': false, 'penalty': -2}, 
                         {'min': 13, 'max': 16, 'status': 'Mortal 0', 'stun': true, 'death': true, 'penalty': -3}, 
                         {'min': 17, 'max': 20, 'status': 'Mortal 1', 'stun': true, 'death': true, 'penalty': -4}, 
                         {'min': 21, 'max': 24, 'status': 'Mortal 2', 'stun': true, 'death': true, 'penalty': -5}, 
                         {'min': 25, 'max': 28, 'status': 'Mortal 3', 'stun': true, 'death': true, 'penalty': -6}, 
                         {'min': 29, 'max': 32, 'status': 'Mortal 4', 'stun': true, 'death': true, 'penalty': -7}, 
                         {'min': 33, 'max': 36, 'status': 'Mortal 5', 'stun': true, 'death': true, 'penalty': -8}, 
                         {'min': 37, 'max': 40, 'status': 'Mortal 6', 'stun': true, 'death': true, 'penalty': -9},
                         {'min': 41, 'max': 1000, 'status': 'Fallecido', 'stun': true, 'death': true, 'penalty': -10}];
    let damageTypes =   [{'type': 'Normal', 'CPB': 1, 'CPD': 1, 'damage': 1},
                         {'type': 'Perforante', 'CPB': 1, 'CPD': 0.5, 'damage': 0.5}, 
                         {'type': 'Filo', 'CPB': 0.5, 'CPD': 1, 'damage': 1}, 
                         {'type': 'Monofilo', 'CPB': 0.666, 'CPD': 0.333, 'damage': 1},
                         {'type': 'HEAT', 'CPB': 1, 'CPD': 0.5, 'damage': 1},
                         {'type': 'EAP', 'CPB': 1, 'CPD': 0.25, 'damage': 0.5},
                         {'type': 'Flechas', 'CPB': 0.5, 'CPD': 0.5, 'damage': 1},
                         {'type': 'Electrotermal', 'CPB': 1, 'CPD': 1, 'damage': 1.5}];
    return {
        'localization': localizations, 
        'healthStatus': healthStatus, 
        'damageTypes': damageTypes
    };
}

// Tools for Life Path
function getRandomElementFrom(arrayValues) {
    let selected = Math.floor(Math.random() * arrayValues.length);
    return arrayValues[selected];
}

function generateStyleLifePath() {
    let lifepathEthnicTables = lifepathTables['Ethnic'];
    let lifepathStyleTables = lifepathTables['Style'];

    let originObject = getRandomElementFrom(lifepathEthnicTables['Origin']);
    $('#lifepath_origin').val(originObject['ethnic']);
    $('#lifepath_languages').val(originObject['languages']);

    let clothesObject = getRandomElementFrom(lifepathStyleTables['Clothes']);
    $('#lifepath_clothes').val(clothesObject['clothes']);
    let hairObject = getRandomElementFrom(lifepathStyleTables['Hair']);
    $('#lifepath_hair').val(hairObject['hair']);
    let traitsObject = getRandomElementFrom(lifepathStyleTables['Traits']);
    $('#lifepath_traits').val(traitsObject['traits']);
}

function generateMotivationsLifePath() {
    let lifepathMotivationsTables = lifepathTables['Motivations'];

    let personalityObject = getRandomElementFrom(lifepathMotivationsTables['Personality']);
    $('#lifepath_personality').val(personalityObject['personality']);
    let mostValuedPersonObject = getRandomElementFrom(lifepathMotivationsTables['MostValuedPerson']);
    $('#lifepath_most_valued_person').val(mostValuedPersonObject['person']);
    let mostValuableObject = getRandomElementFrom(lifepathMotivationsTables['MostValuable']);
    $('#lifepath_most_valuable').val(mostValuableObject['value']);
    let mostValuedThingObject = getRandomElementFrom(lifepathMotivationsTables['MostValuedThing']);
    $('#lifepath_most_valued_thing').val(mostValuedThingObject['thing']);
    let peopleOpinionObject = getRandomElementFrom(lifepathMotivationsTables['PeopleOpinion']);
    $('#lifepath_people_opinion').val(peopleOpinionObject['opinion']);
}

function addSiblingRow(row) {
    let newRow = '<tr class="lifepath_siblings_row">' +
            '<td>' + row + '</td>' +
            '<td><input class="form-control" type="text" id="lifepath_sibling_gender_' + row + '" readonly="yes"/></td>' +
            '<td><input class="form-control" type="text" id="lifepath_sibling_order_' + row + '" readonly="yes"/></td>' +
            '<td><input class="form-control" type="text" id="lifepath_sibling_relationship_' + row + '" readonly="yes"/></td>' +
        '</tr>';
    $('#lifepath_siblings>tbody').append(newRow);    
}

function generateFamilyLifePath() {
    let lifepathFamilyTables = lifepathTables['Family'];

    let familyClassObject = getRandomElementFrom(lifepathFamilyTables['Class']);
    $('#lifepath_class').val(familyClassObject['class'] + '. ');
    let parentsObject = getRandomElementFrom(lifepathFamilyTables['Parents']);
    $('#lifepath_parents').val(parentsObject['parents'] + '. ');
    if (lifepathFamilyTables['Parents'].indexOf(parentsObject) >= 6) {
        let parentTragedyObject = getRandomElementFrom(lifepathFamilyTables['ParentTragedy']);
        $('#lifepath_parents').val(parentTragedyObject['parent_tragedy'] + '. ');
    }
    let familySituationObject = getRandomElementFrom(lifepathFamilyTables['FamilySituation']);
    $('#lifepath_family_situation').val(familySituationObject['family_situation'] + '. ');
    if (lifepathFamilyTables['FamilySituation'].indexOf(familySituationObject) <= 5) {
        let familyTragedyObject = getRandomElementFrom(lifepathFamilyTables['FamilyTragedy']);
        $('#lifepath_family_situation').val(familyTragedyObject['family_tragedy'] + '. ');
    }
    let childhoodObject = getRandomElementFrom(lifepathFamilyTables['Childhood']);
    $('#lifepath_childhood').val(childhoodObject['childhood'] + '. ');

    $('#lifepath_siblings tbody').empty();
    let siblingsObject = getRandomElementFrom(lifepathFamilyTables['SiblingsQuantity']);
    if (parseInt(siblingsObject['quantity']) > 0) {
        let quantity = parseInt(siblingsObject['quantity']);
        $('#lifepath_siblings caption').text('Tiene ' + quantity + ' hermanos.');
        for (let i = 1; i <= quantity; i++ ) {
            addSiblingRow(i);
            $('#lifepath_sibling_gender_' + i).val(getRandomElementFrom(lifepathFamilyTables['SiblingGender'])['gender']);
            $('#lifepath_sibling_order_' + i).val(getRandomElementFrom(lifepathFamilyTables['SiblingOrder'])['order']);
            $('#lifepath_sibling_relationship_' + i).val(getRandomElementFrom(lifepathFamilyTables['SiblingRelationship'])['relationship']);
        }
    }
    else 
        $('#lifepath_siblings caption').text('No tiene hermanos.');

}

function getRandomAge() {
    let age = 18 + Math.floor(Math.random() * 11);
    $('#lifepath_age').val(age);
}

function addEventRow(row) {
    let newRow = '<tr class="lifepath_events_row">' +
            '<td>' + row + '</td>' +
            '<td><input class="form-control" type="text" id="lifepath_event_description_' + row + '" readonly="yes"/></td>' +
        '</tr>';
    $('#lifepath_events>tbody').append(newRow);    
}

function generateEventsLifePath() {
    if ($('#lifepath_age').val() == '') {
        alert('Ingrese su edad para calcular los eventos de su vida.');
        return;
    }
    let age = parseInt($('#lifepath_age').val());
    if (age < 18) {
        alert('Su edad debe ser mayor o igual a 18 años.');
        return;
    }

    let lifepathEventTables = lifepathTables['Events'];

    $('#lifepath_events tbody').empty();
    for (let i = 16; i < age; i++) {
        addEventRow(i);
        let eventObject = getRandomElementFrom(lifepathEventTables['TypeOfEvent']);
        let eventDescription = 'Nada importante';
        if (eventObject['next'] != '') {
            let typeOfEvent = eventObject['next'];
            let eventDetailObject = getRandomElementFrom(lifepathEventTables[typeOfEvent]);
            let keyName = Object.keys(eventDetailObject)[0];
            eventDescription = eventDetailObject[keyName];
        }
        $('#lifepath_event_description_' + i).val(eventDescription);
    }
    addEventRow(age);
    $('#lifepath_event_description_' + age).val('EL PRESENTE');
}

// Tools for Armor Functions
function addArmorRow() {
    armorRows++;
    let newRow = '<tr class="armor_form_row">' +
                '<td>' + armorRows + '</td>' +
                '<td><input class="form-control" type="text" id="armor_name_' + armorRows + '"/></td>' +
                '<td><select class="form-control" id="armor_type_' + armorRows + '" onchange="calculateArmor(' + armorRows + ')">' + fillArmorTypeSelect() + '</select></td>' +
                '<td><select class="form-control" id="armor_coverage_' + armorRows + '" onchange="calculateArmor(' + armorRows + ')">' + fillCoverageSelect() + '</select></td>' +
                '<td><input class="form-control" type="text" id="armor_cp_' + armorRows + '" onchange="calculateArmor(' + armorRows + ')"/></td>' +
                '<td><input class="form-control" type="text" id="armor_ce_' + armorRows + '" onchange="calculateArmor(' + armorRows + ')"/></td>' +
             '</tr>';
    $('#armor_table>tbody').append(newRow);
}

function fillArmorTypeSelect() {
    let selectList = '<option>Seleccione</option>';
    let armorTypes = armorTables['armorTypes'];
    let pos = 0;
    armorTypes.forEach(armorType => {
        selectList += '<option value="' + pos + '">' + 
                        armorType['type'] +
                      '</option>';
        pos++;
    });
    return selectList;
}

function fillCoverageSelect() {
    let selectList = '<option>Seleccione</option>';
    let armorCoverages = armorTables['coverage'];
    let pos = 0;
    armorCoverages.forEach(coverage => {
        selectList += '<option value="' + pos + '">' + 
                        coverage['cover'] +
                      '</option>';
        pos++;
    });
    return selectList;
}

function calculateArmor(row) {
    if ($('#armor_type_' + row).val() == '' || $('#armor_coverage_' + row).val() == '' || $('#armor_cp_' + row).val() == '' || $('#armor_ce_' + row).val() == '') return;
    let localizedArmor = [
        {'from': 1, 'to': 1, 'locale': 'Cabeza', 'armor_cpb':[], 'armor_cpd':[], 'armor_ce':[]},
        {'from': 2, 'to': 4, 'locale': 'Torso', 'armor_cpb':[], 'armor_cpd':[], 'armor_ce':[]}, 
        {'from': 5, 'to': 5, 'locale': 'Brazo Izquierdo', 'armor_cpb':[], 'armor_cpd':[], 'armor_ce':[]},
        {'from': 6, 'to': 6, 'locale': 'Brazo Derecho', 'armor_cpb':[], 'armor_cpd':[], 'armor_ce':[]},
        {'from': 7, 'to': 8, 'locale': 'Pierna Izquierda', 'armor_cpb':[], 'armor_cpd':[], 'armor_ce':[]},
        {'from': 9, 'to': 10, 'locale': 'Pierna Derecha', 'armor_cpb':[], 'armor_cpd':[], 'armor_ce':[]}
    ];
    let actualCE = 0;
    localizedArmor.forEach(armor => {
        let localizedFrom = armor['from'];
        let localizedTo = armor['to'];
        for (let i = 1; i <= armorRows; i++) {
            let armorType = armorTables['armorTypes'][$('#armor_type_' + i).val()];
            let coverage = armorTables['coverage'][$('#armor_coverage_' + i).val()];
            let coverageFrom = coverage['from'];
            let coverageTo = coverage['to'];
            if (coverageFrom >= localizedFrom && coverageFrom <= localizedTo || 
                coverageTo >= localizedFrom && coverageTo <= localizedTo ||
                localizedFrom >= coverageFrom && localizedFrom <= coverageTo || 
                localizedTo >= coverageFrom && localizedTo <= coverageTo) {
                    armor['armor_' + armorType['code']].push(parseInt($('#armor_cp_' + i).val()));
                    armor['armor_ce'].push(parseInt($('#armor_ce_' + i).val()));
            }
        }

        let localizedCPB = 0;
        let armorCountB = 0;
        armor['armor_cpb'].sort(function(a, b){return b - a;});
        armor['armor_cpb'].forEach(cpValue => {
            if (armorCountB == 0) localizedCPB = cpValue;
            else localizedCPB = calculateMixedCP(localizedCPB, cpValue);
            armorCountB++;
        });

        let localizedCPD = 0;
        let armorCountD = 0;
        armor['armor_cpd'].sort(function(a, b){return b - a;});
        armor['armor_cpd'].forEach(cpValue => {
            if (armorCountD == 0) localizedCPD = cpValue;
            else localizedCPD = calculateMixedCP(localizedCPD, cpValue);
            armorCountD++;
        });

        armorTables['damageTypes'].forEach(damageType =>{
            let localizedCP = 0;
            if (armorCountB > 0 && armorCountD > 0) {
                localizedCP = calculateMixedCP(localizedCPB * damageType['CPB'], localizedCPD * damageType['CPD']);
            }
            else if (armorCountB > 0) localizedCP = localizedCPB * damageType['CPB'];
            else if (armorCountD > 0) localizedCP = localizedCPD * damageType['CPD'];    
            $('#' + damageType['code'] + '_locale_' + localizedFrom).val(Math.ceil(localizedCP));
        });

        let armorCount = armorCountB + armorCountD;
        let localizedCE = 0;
        armor['armor_ce'].forEach(ceValue => {
            localizedCE += ceValue;
        });
        if (armorCount > 3) localizedCE -= armorCount - 3;
        if (actualCE > localizedCE) actualCE = localizedCE;
    });
    $('#armor_ce').val(actualCE);
}

// Tools for Brawling Functions
function addBrawlingRow() {
    brawlingRows++;
    let newRow = '<tr class="brawling_form_row">' +
                '<td>' + brawlingRows + '</td>' +
                '<td><select class="form-control" id="brawling_technique_' + brawlingRows + '" onchange="calculateBrawlingTecniques(' + brawlingRows + ')">' + fillBrawlingTechniqueSelect() + '</select></td>' +
                '<td><input class="form-control" type="text" id="brawling_level_' + brawlingRows + '" value="0" onchange="calculateBrawlingTecniques(' + brawlingRows + ')"/></td>' +
             '</tr>';
    $('#brawling_table>tbody').append(newRow);
}

function fillBrawlingTechniqueSelect() {
    let selectList = '<option>Seleccione</option>';
    let brawlingTechniques = brawlingTables['martials'];
    let pos = 0;
    brawlingTechniques.forEach(brawlingTechnique => {
        selectList += '<option value="' + pos + '">' + 
                        brawlingTechnique['name'] +
                        ' (' + brawlingTechnique['difficult'] + ')' +
                      '</option>';
        pos++;
    });
    return selectList;
}

function calculateBrawlingTecniques(row) {
    if ($('#brawling_technique_' + row).val() == '' || $('#brawling_level_' + row).val() == '') return;
    let techniquesLevels = [
        {'name': 'barrier', 'value': 0},
        {'name': 'block', 'value': 0},
        {'name': 'disarm', 'value': 0},
        {'name': 'dodge', 'value': 0},
        {'name': 'feint', 'value': 0},
        {'name': 'grapple', 'value': 0},
        {'name': 'kick', 'value': 0},
        {'name': 'prone', 'value': 0},
        {'name': 'punch', 'value': 0},
        {'name': 'quarry', 'value': 0},
        {'name': 'strangle', 'value': 0},
        {'name': 'throw', 'value': 0},
        {'name': 'weapon', 'value': 0}
    ]
    for(let i = 1; i <= brawlingRows; i++) {
        let brawlingTechniques = [];
        let selectedTechnique = '';
        if (i < 4) {
            brawlingTechniques = brawlingTables['abilities'];
            selectedTechnique = $('#brawling_technique_' + i).val();
        }
        else {
            brawlingTechniques = brawlingTables['martials'];
            selectedTechnique = $('#brawling_technique_' + i + ' option:selected').text();
        }
        let match = selectedTechnique.match(/^(.*?)\s*\((\d+)\)$/);
        let techniqueName = match[1];
        let techniqueDifficult = parseInt(match[2]);
        let techniqueLevel = parseInt($('#brawling_level_' + i).val());
        let factor = Math.ceil(techniqueLevel / techniqueDifficult)
        brawlingTechniques.forEach(technique => {
            if (technique['name'] == techniqueName) {
                for(let j = 0; j < 13; j++)
                    techniquesLevels[j]['value'] += technique['techniques'][j]['value'] * factor;
            }
        });
    }
    techniquesLevels.forEach(technique => {
        $('#brawling_technique_' + technique['name']).val(technique['value']);
    });
}

// Tools for Damage Functions
function addDamageRow() {
    damageRows++;
    let newRow = '<tr class="damage_form_row">' +
                '<td>' + damageRows + '</td>' +
                '<td><select class="form-control" id="damage_locale_' + damageRows + '" onchange="calculateActualCP(' + damageRows + ')">' + fillLocalizationSelect() + '</select></td>' +
                '<td><select class="form-control" id="damage_type_' + damageRows + '" onchange="calculateDamage(' + damageRows + ')">' + fillDamageTypeSelect() + '</select></td>' +
                '<td><input class="form-control" type="text" id="damage_value_' + damageRows + '" onchange="calculateDamage(' + damageRows + ')"/></td>' +
                '<td><input class="form-control" type="text" id="damage_cp_' + damageRows + '" readonly="yes"/></td>' +
                '<td><input class="form-control" type="text" id="damage_calculated_' + damageRows + '" readonly="yes"/></td>' +
                '<td><input class="form-control" type="text" id="damage_accumulate_' + damageRows + '" readonly="yes"/></td>' +
                '<td><input class="form-control" type="text" id="damage_woundlevel_' + damageRows + '" readonly="yes"/></td>' +
                '<td><input class="form-control" type="text" id="damage_result_' + damageRows + '" readonly="yes"/></td>' +
             '</tr>';
    $('#damage_table>tbody').append(newRow);
}

function fillLocalizationSelect() {
    let selectList = '<option>Seleccione</option>';
    let localizationArray = damageTables['localization'];
    let pos = 0;
    localizationArray.forEach(localization => {
        selectList += '<option value="' + pos + '">' + 
                        localization['locale'] + 
                        ' (' + localization['rollFrom'];
        if (localization['rollFrom'] < localization['rollTo'])
            selectList +=   '-' + localization['rollTo'];
        selectList +=   ')</option>';
        pos++;
    });
    return selectList;
}

function fillDamageTypeSelect() {
    let selectList = '<option>Seleccione</option>';
    let damageArray = damageTables['damageTypes'];
    let pos = 0;
    damageArray.forEach(damageType => {
        selectList += '<option value="' + pos + '">' + 
                        damageType['type'] + 
                        ' (' + 
                            'CPB x' + damageType['CPB'] + ', ' +
                            'CPD x' + damageType['CPD'] + ', ' +
                            'Daño x' + damageType['damage'] * 100 + '%' +
                        ')' + 
                      '</option>';
        pos++;
    });
    return selectList
}

function calculateMTCandSAVE(stun_mod, death_mod) {
    let body = parseInt($('#BODY').val());
    let mtc = 0;
    let save = body;
    if (body > 10) mtc = -5;
    else if (body > 9) mtc = -4;
    else if (body > 7) mtc = -3;
    else if (body > 4) mtc = -2;
    else if (body > 2) mtc = -1;
    else mtc = 0;
    $('#MTC').val(mtc);
    let stun_save = save + stun_mod;
    if (stun_save < 1) stun_save = 1;
    $('#stun_save').val(stun_save);
    if (death_mod !== false) {
        let death_save = save + death_mod;
        if (death_save < 1) death_save = 1;
        $('#death_save').val(death_save);
    }
    else 
        $('#death_save').val('');
}

let armor = { 
    'cpb': 0, 
    'cpd': 0, 
    'cp': 0 
};

function calculateActualCP(row) {
    let locale = damageTables['localization'][$('#damage_locale_' + row).val()];
    let pos = locale['rollFrom'];
    armor['cpb'] = parseInt($('#cpb_locale_' + pos).val());
    armor['cpd'] = parseInt($('#cpd_locale_' + pos).val());
    let cpmod = 0;
    if ($('#cp_locale_' + pos + '_mod').val() != '')
        cpmod = parseInt($('#cp_locale_' + pos + '_mod').val());
    armor['cp'] = calculateMixedCP(armor['cpb'], armor['cpd']) + cpmod;
    $('#damage_cp_' + row).val(armor['cp']);
}

function checkWoundLevel(totalDamage) {
    let woundLevels = damageTables['healthStatus'];
    let actualWoundLevel = {};
    try { 
        woundLevels.forEach(woundLevel => {
            if (parseInt(woundLevel['min']) <= totalDamage && parseInt(woundLevel['max']) >= totalDamage) {
                actualWoundLevel = woundLevel;
                throw new Error('Stop foreach');
            }
        });
    }
    catch (error) {
        // Nothing to do
    }
    return actualWoundLevel;
}

function sumarizeLocalizedHits(pos) {
    let hits = 0;
    for (let i = 1; i <= damageRows; i++) {
        let locale = damageTables['localization'][$('#damage_locale_' + i).val()];
        if (locale['rollFrom'] == pos) hits++;
    }
    return hits;
}

function calculateDamage(row) {
    let mtc = parseInt($('#MTC').val());
    let locale = damageTables['localization'][$('#damage_locale_' + row).val()];
    let pos = locale['rollFrom'];
    let damageType = damageTables['damageTypes'][$('#damage_type_' + row).val()];
    let damageValue = parseInt($('#damage_value_' + row).val());

    calculateActualCP(row);
    let actualMixedCP = Math.ceil(calculateMixedCP(armor['cpb'] * damageType['CPB'], armor['cpd'] * damageType['CPD']));
    $('#damage_cp_' + row).val(actualMixedCP);

    if ($('#damage_type_' + row).val() == '' || $('#damage_value_' + row).val() == '') return;

    let damageAfterCP = damageValue - actualMixedCP;
    let realDamage = 0; 
    if (damageAfterCP > 0) {
        realDamage = Math.round(damageAfterCP * damageType['damage'] * locale['factor']) + mtc;
        if (realDamage < 1) realDamage = 1;
        $('#damage_result_' + row).val('');
        if (realDamage >= 8) $('#damage_result_' + row).val(locale['result']);
    }
    $('#damage_calculated_' + row).val(realDamage);

    let cpmod = 0;
    if ($('#cp_locale_' + pos + '_mod').val() != '')
        cpmod = parseInt($('#cp_locale_' + pos + '_mod').val());
    $('#cp_locale_' + pos + '_mod').val(- sumarizeLocalizedHits(pos));

    let accDamage = 0;
    if (row > 1) {
        accDamage = parseInt($('#damage_accumulate_' + (row - 1)).val());
    }
    let totalDamage = accDamage + realDamage;
    $('#damage_accumulate_' + row).val(totalDamage);

    let actualWoundLevel = checkWoundLevel(totalDamage);
    let penalty = parseInt(actualWoundLevel['penalty']);
    $('#damage_woundlevel_' + row).val(actualWoundLevel['status'] + ' (' + penalty + ')');
    if (actualWoundLevel['death'])
        calculateMTCandSAVE(penalty, penalty + 3);
    else
        calculateMTCandSAVE(penalty, false);

    let REF = parseInt($('#REF').val());
    let INT = parseInt($('#INT').val());
    let FRI = parseInt($('#FRI').val());
    if (penalty < -9) {
        $('#REF_mod').val(0);
        $('#INT_mod').val(0);
        $('#FRI_mod').val(0);
    }
    else if (penalty < -2) {
        $('#REF_mod').val(Math.ceil(REF / 3));
        $('#INT_mod').val(Math.ceil(INT / 3));
        $('#FRI_mod').val(Math.ceil(FRI / 3));
    }
    else if (penalty < -1) {
        $('#REF_mod').val(Math.ceil(REF / 2));
        $('#INT_mod').val(Math.ceil(INT / 2));
        $('#FRI_mod').val(Math.ceil(FRI / 2));
    }
    else if (penalty < 0) {
        $('#REF_mod').val(REF - 2);
        $('#INT_mod').val(INT);
        $('#FRI_mod').val(FRI);
    }
}