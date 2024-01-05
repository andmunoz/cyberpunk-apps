const SERVERAPI = "https://cyberpunk-database.firebaseio.com/";

function loadData(route, title, hasData) {
    toggleVisibility("#section_content", "#spinner");

    $("#dataTitle").text(title);

    if (hasData) {
        $("#dataResults").DataTable().destroy();
        $("#dataResults>tbody").text("")
    }

    $.ajax({  
        type: "GET",  
        url: SERVERAPI + route + ".json",    
        dataType: "json", 
        success: function (data) {  
            $.each(data, function(i, item){
                let row = "<tr>"+
                "<td>" + item.id + "</td>" + 
                "   <td>" + item.name + "</td>" +
                "   <td>" + item.description + "</td>" +
                "   <td class=\"text-end\">" + item.cost + " creds</td>" +
                "   <td>" +
                "       <button class=\"btn btn-primary\" type=\"button\" data-bs-toggle=\"modal\" data-bs-target=\"#viewItem" + item.id + "Modal\"><i class=\"fa-solid fa-eye\"></i></button>" + 
                "       " + constructModal(item) + 
                "   </td>" +
                "</tr>";						 
                $("#dataResults>tbody").append(row);
            });

            $("#dataResults").DataTable({
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

            toggleVisibility("#spinner", "#section_content");
        }, 
    });         
}

function toggleVisibility(id1, id2) {
    $(id1).hide();
    $(id2).show();
}

function constructModal(item) {
    let modalHTML = "<div class=\"modal fade\" id=\"viewItem" + item.id + "Modal\" tabindex=\"-1\" aria-labelledby=\"viewItem" + item.id + "ModalLabel\" aria-hidden=\"true\">" +
                    "    <div class=\"modal-dialog modal-lg\">" +
                    "       <div class=\"modal-content\">" +
                    "           <div class=\"modal-header\">" +
                    "               <h1 class=\"modal-title fs-5\" id=\"viewItem" + item.id + "ModalLabel\">" + item.name + "</h1>" +
                    "                    <button type=\"button\" class=\"btn-close\" data-bs-dismiss=\"modal\" aria-label=\"Cerrar\"></button>" +
                    "                </div>" +
                    "                <div class=\"modal-body\">" +
                    "                    <div class=\"mb-3\">" +
                    "                        <table class=\"table table-borderless\">" +
                    "                            <caption>&nbsp;</caption>" +
                    "                            <tbody>";
    $.each(item, function(key, value){
        modalHTML += "                                <tr>" +
                    "                                    <th scope=\"row\" class=\"text-end\">" + key + "</td>" +
                    "                                    <td>" + value + "</td>" +
                    "                                </tr>"
    });
                
    modalHTML +=    "                            </tbody>" +
                    "                        </table>" +
                    "                    </div>" +
                    "                </div>" +
                    "                <div class=\"modal-footer\">" +
                    "                    <button type=\"button\" class=\"btn btn-secondary\" data-bs-dismiss=\"modal\">Cerrar</button>" +
                    "                </div>" +
                    "            </div>" +
                    "        </div>" +
                    "    </div>";
    return modalHTML;
}