$(document).ready(function() {

(function ($) {

    var bar = $("#progressbar")[0];
    
    UIkit.upload('.file-upload', {

        url: $("input").attr("target"),
        multiple: false,
        name: $("input").attr("name"),
        params: {
                    csrfmiddlewaretoken: $("input[name=\"csrfmiddlewaretoken\"]").val(),
            },

        /*
        beforeSend: function() { console.log('beforeSend', arguments); },
        beforeAll: function() { console.log('beforeAll', arguments); },
        load: function() { console.log('load', arguments); },
        error: function() { console.log('error', arguments); },
        complete: function() { console.log('complete', arguments); },
        */

        loadStart: function (e) {
            bar.removeAttribute('hidden');
            bar.max =  e.total;
            bar.value =  e.loaded;
        },

        progress: function (e) {
            bar.max =  e.total;
            bar.value =  e.loaded;
        },

        loadEnd: function (e) {
            bar.max =  e.total;
            bar.value =  e.loaded;
        },

        completeAll: function () {
            setTimeout(function () {
                bar.setAttribute('hidden', 'hidden');
                location.reload();
            }, 1000);
        }
    });

})(jQuery); 

});
