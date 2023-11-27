function ajax_get_token() {
    // Fetch data from the server using AJAX// Fetch data from the server using AJAX
        $.ajax({
            url: '{% url "fortiwan_monitor:fetch_tunnels" %}',
            type: 'GET',
            dataType: 'json',
            success: function (dataList) {
                // Hide spinner on success and display data
                $('#spinner').hide();

                // Loop through the list of VPN tunnels
                $.each(dataList, function (index, data) {
                    // Clone the template for each VPN tunnel
                    var $template = $('#template').clone();
      
                    $template.find('#ipsec-name').text(data.name + ' | ' + data.comment);

                    $template.find('#ipsec-status').text('STATUS ' + data.status.toUpperCase());

                    $template.find('#ipsec-ip').text(data.ip);

                    $template.find('#ipsec-incoming-core').text(data.incoming_core);
                    $template.find('#ipsec-incoming-tunnel').text(data.incoming_tunnel);

                    $template.find('#ipsec-outgoing-core').text(data.outgoing_core);
                    $template.find('#ipsec-outgoing-tunnel').text(data.outgoing_tunnel);

                    var wan_interface = data.interface;                    
                    console.log(wan_interface);

                    if (wan_interface == 'ECHO') {
                        $template.find('#has-interface').text('ECHO').show();          
                        $template.find('#no-interface').hide();

                        var $modal = $('#modal-template').clone();

                        var interface_modal_id = 'interface-modal-' + data.name.toLowerCase();

                        $modal.find('#interface-modal').attr('id', interface_modal_id);
                        $modal.find('#modal-title').text('Switch to MTN Interface?');
                        $modal.find('#interface-desc').text('Are you sure you want switch ' + data.name + ' from ECHO to MTN');


                        var $launch_modal = $('#launch-modal').clone();

                        $launch_modal.attr('data-bs-target', '#' + interface_modal_id);
                        $launch_modal.attr('title', interface_modal_id + '-title');
                        $launch_modal.text('Switch Interfaces').removeAttr('hidden');
                        $launch_modal.attr('id', interface_modal_id + '-launch-modal');

                        $template.find('#card-footer').append($launch_modal);

                        $modal.find('#modal-save').attr('onclick', "confirmSwitch('" + data.name + "', '" + wan_interface + "')")
                        
                        // $modal.find('#modal-form').attr('action', '{% url "fortiwan_config:put_interface" %}')
                        $modal.find('#input-interface-name').attr('value', data.name)
                        $modal.find('#input-interface').attr('value', wan_interface)

                        $('#modal-container').append($modal);

                    } else if (wan_interface == 'MTN') {
                        $template.find('#has-interface').text('MTN').show();          
                        $template.find('#no-interface').hide();

                        var $modal = $('#modal-template').clone();

                        var interface_modal_id = 'interface-modal-' + data.name.toLowerCase();

                        $modal.find('#interface-modal').attr('id', interface_modal_id);
                        $modal.find('#modal-title').text('Switch to ECHO Interface?');
                        $modal.find('#interface-desc').text('Are you sure you want switch <b>' + data.name + '</b> from MTN to ECHO');

                        var $launch_modal = $('#launch-modal').clone();

                        $launch_modal.attr('data-bs-target', '#' + interface_modal_id);
                        $launch_modal.attr('title', interface_modal_id + '-title');
                        $launch_modal.text('Switch Interfaces').removeAttr('hidden');
                        $launch_modal.attr('id', interface_modal_id + '-launch-modal');                        

                        $template.find('#card-footer').append($launch_modal);
                        $modal.find('#modal-save').attr('onclick', "confirmSwitch('" + data.name + "', '" + wan_interface + "')")

                        $('#modal-container').append($modal);
                    } else {
                        $template.find('#no-interface').show();
                        $template.find('#edit-model-btn').addClass('disabled');
                    }

                    // Remove the hidden Attribute for VPN/IPsec Tunnel
                    $template.removeAttr('hidden');

                    // Populate VPN/IPsec Container
                    $('#ipsec-container').append($template);
                });
            
            },
            error: function () {
                // Handle errors if necessary
                console.error('Error fetching data from the server');
            }
        });      
    $.ajax({
        url: '{% url "fortiwan_monitor:fetch_tunnels" %}',
        type: 'GET',
        dataType: 'json',
        success: function (dataList) {
            // Hide spinner on success and display data
            $('#spinner').hide();

            // Loop through the list of VPN tunnels
            $.each(dataList, function (index, data) {
                // Clone the template for each VPN tunnel
                var $template = $('#template').clone();
  
                $template.find('#ipsec-name').text(data.name + ' | ' + data.comment);

                $template.find('#ipsec-status').text('STATUS ' + data.status.toUpperCase());

                $template.find('#ipsec-ip').text(data.ip);

                $template.find('#ipsec-incoming-core').text(data.incoming_core);
                $template.find('#ipsec-incoming-tunnel').text(data.incoming_tunnel);

                $template.find('#ipsec-outgoing-core').text(data.outgoing_core);
                $template.find('#ipsec-outgoing-tunnel').text(data.outgoing_tunnel);

                var wan_interface = data.interface;                    
                console.log(wan_interface);

                if (wan_interface == 'ECHO') {
                    $template.find('#has-interface').text('ECHO').show();          
                    $template.find('#no-interface').hide();

                    var $modal = $('#modal-template').clone();

                    var interface_modal_id = 'interface-modal-' + data.name.toLowerCase();

                    $modal.find('#interface-modal').attr('id', interface_modal_id);
                    $modal.find('#modal-title').text('Switch to MTN Interface?');
                    $modal.find('#interface-desc').text('Are you sure you want switch ' + data.name + ' from ECHO to MTN');


                    var $launch_modal = $('#launch-modal').clone();

                    $launch_modal.attr('data-bs-target', '#' + interface_modal_id);
                    $launch_modal.attr('title', interface_modal_id + '-title');
                    $launch_modal.text('Switch Interfaces').removeAttr('hidden');
                    $launch_modal.attr('id', interface_modal_id + '-launch-modal');

                    $template.find('#card-footer').append($launch_modal);

                    $modal.find('#modal-save').attr('onclick', "confirmSwitch('" + data.name + "', '" + wan_interface + "')")
                    
                    // $modal.find('#modal-form').attr('action', '{% url "fortiwan_config:put_interface" %}')
                    $modal.find('#input-interface-name').attr('value', data.name)
                    $modal.find('#input-interface').attr('value', wan_interface)

                    $('#modal-container').append($modal);

                } else if (wan_interface == 'MTN') {
                    $template.find('#has-interface').text('MTN').show();          
                    $template.find('#no-interface').hide();

                    var $modal = $('#modal-template').clone();

                    var interface_modal_id = 'interface-modal-' + data.name.toLowerCase();

                    $modal.find('#interface-modal').attr('id', interface_modal_id);
                    $modal.find('#modal-title').text('Switch to ECHO Interface?');
                    $modal.find('#interface-desc').text('Are you sure you want switch <b>' + data.name + '</b> from MTN to ECHO');

                    var $launch_modal = $('#launch-modal').clone();

                    $launch_modal.attr('data-bs-target', '#' + interface_modal_id);
                    $launch_modal.attr('title', interface_modal_id + '-title');
                    $launch_modal.text('Switch Interfaces').removeAttr('hidden');
                    $launch_modal.attr('id', interface_modal_id + '-launch-modal');                        

                    $template.find('#card-footer').append($launch_modal);
                    $modal.find('#modal-save').attr('onclick', "confirmSwitch('" + data.name + "', '" + wan_interface + "')")

                    $('#modal-container').append($modal);
                } else {
                    $template.find('#no-interface').show();
                    $template.find('#edit-model-btn').addClass('disabled');
                }

                // Remove the hidden Attribute for VPN/IPsec Tunnel
                $template.removeAttr('hidden');

                // Populate VPN/IPsec Container
                $('#ipsec-container').append($template);
            });
        
        },
        error: function () {
            // Handle errors if necessary
            console.error('Error fetching data from the server');
        }
    }); 
};