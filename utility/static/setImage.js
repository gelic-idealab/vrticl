AFRAME.registerComponent('set-image', {
      schema: {
        on: {type: 'string'},
        target: {type: 'selector'},
        src: {type: 'string'},
        dur: {type: 'number', default: 800}
      },
      init: function () {
        var data = this.data;
        var el = this.el;

        this.setupFadeAnimation();

        if(current.right == null)document.querySelector('#goRightLink').setAttribute("visible", false);
        else document.getElementById('goRightLink').setAttribute("visible", true);
        if(current.left == null) document.getElementById('goLeftLink').setAttribute("visible", false);
        else document.getElementById('goLeftLink').setAttribute("visible", true);
        if(current.forward == null) document.getElementById('goForwardLink').setAttribute("visible", false);
        else document.getElementById('goForwardLink').setAttribute("visible", true);
        if(current.backward == null) document.getElementById('goBackwardLink').setAttribute("visible", false);
        else document.getElementById('goBackwardLink').setAttribute("visible", true);


        el.addEventListener(data.on, function () {
            if(current[data.src.split('-')[1]] != null) {
                // Fade out image.
                data.target.emit('set-image-fade');
                console.log(data);
                console.log(el);
                console.log(current);
                // Wait for fade to complete.
                setTimeout(function () {
                    // Set image.
                    data.target.setAttribute('material', 'src', listOfFiles[current[data.src.split('-')[1]]].img);
                    var previous = current;
                    current = listOfFiles[current[data.src.split('-')[1]]];
                    if(current.right == null)document.querySelector('#goRightLink').setAttribute("visible", false);
                    else document.getElementById('goRightLink').setAttribute("visible", true);
                    if(current.left == null) document.getElementById('goLeftLink').setAttribute("visible", false);
                    else document.getElementById('goLeftLink').setAttribute("visible", true);
                    if(current.forward == null) document.getElementById('goForwardLink').setAttribute("visible", false);
                    else document.getElementById('goForwardLink').setAttribute("visible", true);
                    if(current.backward == null) document.getElementById('goBackwardLink').setAttribute("visible", false);
                    else document.getElementById('goBackwardLink').setAttribute("visible", true);

                }, data.dur);
            }
        });
      },

      setupFadeAnimation: function () {
        var data = this.data;
        var targetEl = this.data.target;

        // Only set up once.
        if (targetEl.dataset.setImageFadeSetup) { return; }
        targetEl.dataset.setImageFadeSetup = true;

        // Create animation.
        targetEl.setAttribute('animation__fade', {
          property: 'material.color',
          startEvents: 'set-image-fade',
          dir: 'alternate',
          dur: data.dur,
          from: '#FFF',
          to: '#000'
        });
      }
    });

