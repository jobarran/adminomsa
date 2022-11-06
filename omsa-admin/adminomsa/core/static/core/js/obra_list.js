$(document).ready(function() {
    // Setup - add a text input to each footer cell
    $('#example tfoot th').each( function () {
        var title = $('#example thead th').eq( $(this).index() ).text();
        $(this).html( '<input type="text" placeholder=" '+title+'" />' );
    } );
  
    // DataTable
  var table = $('#example').DataTable( {
    
    stateSave: true,
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
    fixedHeader: true,
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
      
      table.draw(false);
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