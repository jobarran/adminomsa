$(document).ready(function() {
    // Setup - add a text input to each footer cell
    $('#example tfoot th').each( function () {
        var title = $('#example thead th').eq( $(this).index() ).text();
        $(this).html( '<input type="text" placeholder=" '+title+'" />' );
    } );
  
    // DataTable
  var table = $('#example').DataTable( {
    "bStateSave": true,
          "fnStateSave": function (oSettings, oData) {
              localStorage.setItem('offersDataTables', JSON.stringify(oData));
          },
          "fnStateLoad": function (oSettings) {
              return JSON.parse(localStorage.getItem('offersDataTables'));
          },
  language: {
      searchPlaceholder: "Buscar",
      search: "",
      decimal: "",
      emptyTable: "No hay información",
      info: "",
      infoEmpty: "",
      infoFiltered: "",
      infoPostFix: "",
      thousands: ",",
      lengthMenu: "Mostrar _MENU_ Entradas",
      loadingRecords: "Cargando...",
      processing: "Procesando...",
      zeroRecords: "Sin resultados encontrados",
      paginate: {
          first: "Primero",
          last: "Ultimo",
          next: "Siguiente >",
          previous: "< Anterior"
      }
    },
    lengthMenu: [10, 25, 50, 75, 100 ],
    responsive: true,
    orderCellsTop: true,
    fixedHeader: true,
    stateSave: true
  } );
  
    // Restore state
    var state = table.state.loaded();
    if ( state ) {
      table.columns().eq( 0 ).each( function ( colIdx ) {
        var colSearch = state.columns[colIdx].search;
        
        if ( colSearch.search ) {
          $( 'input', table.column( colIdx ).footer() ).val( colSearch.search );
        }
      } );
      
      table.draw();
    }
    
  
    // Apply the search
    table.columns().eq( 0 ).each( function ( colIdx ) {
        $( 'input', table.column( colIdx ).footer() ).on( 'keyup change', function () {
            table
                .column( colIdx )
                .search( this.value )
                .draw();
        } );
    } );
  } );

















  $(document).ready(function() {
     // Setup - add a text input to each footer cell
     $('#example thead tr')
     .clone(true)
     .addClass('filters')
     .appendTo('#example thead');

 var table = $('#example').DataTable({
    language: {
        searchPlaceholder: "Buscar",
        search: "",
        decimal: "",
        emptyTable: "No hay información",
        info: "",
        infoEmpty: "",
        infoFiltered: "",
        infoPostFix: "",
        thousands: ",",
        lengthMenu: "Mostrar _MENU_ Entradas",
        loadingRecords: "Cargando...",
        processing: "Procesando...",
        zeroRecords: "Sin resultados encontrados",
        paginate: {
            first: "Primero",
            last: "Ultimo",
            next: "Siguiente >",
            previous: "< Anterior"
        }
      },
     lengthMenu: [10, 25, 50, 75, 100 ],
     responsive: true,
     orderCellsTop: true,
     fixedHeader: true,
     bStateSave: true,
     initComplete: function () {
         var api = this.api();

         // For each column
         api
             .columns()
             .eq(0)
             .each(function (colIdx) {
                 // Set the header cell to contain the input element
                 var cell = $('.filters th').eq(
                     $(api.column(colIdx).header()).index()
                 );
                 var title = $(cell).text();
                 $(cell).html('<input type="text" placeholder="' + title + '" />');

                 // On every keypress in this input
                 $(
                     'input',
                     $('.filters th').eq($(api.column(colIdx).header()).index())
                 )
                     .off('keyup change')
                     .on('change', function (e) {
                         // Get the search value
                         $(this).attr('title', $(this).val());
                         var regexr = '({search})'; //$(this).parents('th').find('select').val();

                         var cursorPosition = this.selectionStart;
                         // Search the column for that value
                         api
                             .column(colIdx)
                             .search(
                                 this.value != ''
                                     ? regexr.replace('{search}', '(((' + this.value + ')))')
                                     : '',
                                 this.value != '',
                                 this.value == ''
                             )
                             .draw();
                     })
                     .on('keyup', function (e) {
                         e.stopPropagation();

                         $(this).trigger('change');
                         $(this)
                             .focus()[0]
                             .setSelectionRange(cursorPosition, cursorPosition);
                     });
             });
     },


    });

});


