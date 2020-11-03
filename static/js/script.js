$(document).ready(function(){
    $('.sidenav').sidenav();
    $('select').formSelect();

    addingIngredindients()
    function addingIngredindients(){
         let i = 1 
            $("#add_ing").click(function() {
                i++;
                $("#ingred-table").append('<tr id="row'+i+'"> <td><input id="ingredient" type="text" name="ingredients[]" class="validate input-block" required/></td><td><button type="button" class="btn waves-effect waves-light btn-remove" id="'+i+'">X</button></td></tr>');
                $(document).on('click', '.btn-remove', function() {
                        let button_id = $(this).attr("id");
                        $("#row"+button_id+"").remove();
                });
            });
            
    }
  
    addTools() 
    function addTools() {
        let i = 1
        $("#add_tools").click(function() { 
            // return console.log("button clicked")
            i++;
            console.log(i)
            $("#tools-table").append('<tr id="tooltb'+i+'"> <td><input id="tools" type="text" name="tools[]" class="validate input-block" required/></td><td><button class="btn waves-effect waves-light btn-remove" type="button" id="'+i+'">X</button></td></tr>');
            $(document).on('click', '.btn-remove', function() {
                let button_id = $(this).attr("id");
                $("#tooltb"+button_id+"").remove();

            });

        });
    }

    addPrep()
    function addPrep() {
        let i = 1
        $("#add_prep").click(function(){
            i++;
            $("#prep-table").append('<tr id="preptb'+i+'"><td><textarea id="preparation" name="preparation[]" class="materialize-textarea validate" required></textarea></td> <td><button class="btn waves-effect waves-light btn-remove" type="button"  id="'+i+'">X</button></td></tr>');
             $(document).on('click', '.btn-remove', function() {
                let button_id = $(this).attr("id");
                $("#preptb"+button_id+"").remove();

            });
        });
    }
    $(".btn-remove").click(function(){
        $(this).closest("tr").remove();
        console.log("hello")
    });

    // pagination
    pagination()
    function pagination() {
        pageSize = 6

        let pageCount =  $(".recipe-content").length / pageSize;

        for(var i = 0 ; i<pageCount;i++) {
            $(".add-page").append('<li class="waves-effect"><a href="#!">'+(i+1)+'</a></li>');
        }

            $(".add-page li").first().addClass("active")
        showPage = function(page) {
            $(".recipe-content").hide();
            $(".recipe-content").each(function(n) {
                if (n >= pageSize * (page - 1) && n < pageSize * page)
                    $(this).show();
            });        
        }

            showPage(1);

        $(".add-page li").click(function() {
            $(".add-page li").removeClass("active");
            $(this).addClass("active");
            showPage(parseInt($(this).text())) 
        });
    }
    
  });