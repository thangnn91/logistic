$.fn.getType = function() {
    return this[0].tagName == "INPUT" ? this[0].type.toLowerCase() : this[0].tagName.toLowerCase();
}
$(function() {
    $("form").submit(function(event) {
        var that = this;
        event.preventDefault();
        if ($(that).data('function')) {
            window[$(that).data('function')](that);
            return;
        }
        var isError = false;
        var checkDup = [];
        var msgCheckdup = '';
        $('input').each(function() {
            var value = $(this).val();
            var type = $(this).getType();
            if (type === 'checkbox')
                value = $(this).is(':checked') ? value : '';

            if ($(this).hasClass('require') && !value) {
                var msg = $(this).data('require');
                $.toast({
                    heading: 'Có lỗi xảy ra',
                    text: msg,
                    position: 'bottom-right',
                    icon: 'error'
                })
                isError = true;
                return false;
            }

            if ($(this).hasClass('checkdup')) {
                msgCheckdup = $(this).data('checkdup');
                checkDup.push(value);
            }

        });
        if (checkDup.length && !checkDup.every((val, i, arr) => val === arr[0])) {
            $.toast({
                heading: 'Có lỗi xảy ra',
                text: msgCheckdup,
                position: 'bottom-right',
                icon: 'error'
            });
            return;
        }
        if (!isError)
            that.submit();
    });

    window.checkRegisterForm = function(t) {
        alert('vao');
        console.log(t);
    }

    $('a.radio_tab[data-toggle="tab"]').on('shown.bs.tab', function(e) {
    	e.preventDefault();
        var target = $(e.target); // activated tab
        debugger;
        $(target).children('input').is(':disabled')
        	return;
        $(target).children('input').prop('checked', true);
    });
    // $(".form_slider").slider({});

    $('.add_fee').on('click', function() {
        var html = '';
        if ($(this).data('type') == 1)
            html += `<div class="form-group fee_item fee_item_added">
							<label class="col-sm-2 control-label p-t-5">Khoảng
							giá</label>
						<div class="col-sm-10">
							<div class="row">
								<div class="col-md-4">
									<input type="number" class="form-control"
										placeholder="Từ (triệu vnđ)">
								</div>
								<div class="col-md-4">
									<input type="number" class="form-control"
										placeholder="Đến (triệu vnđ)">
								</div>
								<div class="col-md-2">
									<input type="number" class="form-control"
										placeholder="Phí dịch vụ (%)">
								</div>
								<div class="col-md-2">
									<label class="col-sm-2 control-label p-t-5"><a
										href="#" class="p-t-5 rm_fee"><i
											class='fa fa-trash-o icon'></i></a></label>
					
								</div>
							</div>
						</div>
					</div>`;
        else
            html += `<div class="form-group fee_item fee_item_added">
							<label class="col-sm-2 control-label p-t-5">Cân nặng</label>
						<div class="col-sm-10">
							<div class="row">
								<div class="col-md-4">
									<input type="number" class="form-control"
										placeholder="Từ (kg)">
								</div>
								<div class="col-md-4">
									<input type="number" class="form-control"
										placeholder="Đến (kg)">
								</div>
								<div class="col-md-2">
									<input type="number" class="form-control"
										placeholder="Phí dịch vụ (vnđ)">
								</div>
								<div class="col-md-2">
									<label class="col-sm-2 control-label p-t-5"><a
										href="#" class="p-t-5 rm_fee"><i
											class='fa fa-trash-o icon'></i></a></label>
					
								</div>
							</div>
						</div>
					</div>`;
        $(this).parents('.fee_body').append(html);
    });

    $('.fee_body').on('click', '.rm_fee', function() {
        $(this).parents('.fee_item_added').remove();
    });
    
    $('.modal').on('hidden.bs.modal', function () {
        $('input[type="text"],input.data-hidden').val('');
    });
    
    
 // 
    var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    var d1 = [];
    for (var i = 0; i <= 11; i += 1) {
      d1.push([i, parseInt((Math.floor(Math.random() * (1 + 20 - 10))) + 10)]);
    }
    $("#flot-1ine").length && $.plot($("#flot-1ine"), [{
            data: d1
        }], 
        {
          series: {
              lines: {
                  show: true,
                  lineWidth: 2,
                  fill: true,
                  fillColor: {
                      colors: [{
                          opacity: 0.0
                      }, {
                          opacity: 0.2
                      }]
                  }
              },
              points: {
                  radius: 5,
                  show: true
              },
              grow: {
                active: true,
                steps: 50
              },
              shadowSize: 2
          },
          grid: {
              hoverable: true,
              clickable: true,
              tickColor: "#f0f0f0",
              borderWidth: 1,
              color: '#f0f0f0'
          },
          colors: ["#65bd77"],
          xaxis:{
          },
          yaxis: {
            ticks: 5
          },
          tooltip: true,
          tooltipOpts: {
            content: "chart: %x.1 is %y.4",
            defaultTheme: false,
            shifts: {
              x: 0,
              y: 20
            }
          }
        }
    );
})

window.business_function = {
	getBalance: function(){
		$.ajax({
		    url : "/dashboard/user-balance",
		    type : "GET",
		    async: false,
		    success : function(balance) {
		       $('#user_balance').text(formatMoney(balance))
		    },
		    error: function(xhr, ajaxOptions, thrownError) {
		       console.log(xhr.responseText);
		    }
		 });
	},
    changePassword: function(formId) {
        let $form = $('#' + formId);
        let formData = new FormData();
        let oldPass = $form.find('input[name=old_pass]').val();
        if (!oldPass) {
            $.toast({
                heading: 'Có lỗi xảy ra',
                text: 'Vui lòng nhập mật khẩu cũ',
                position: 'bottom-right',
                icon: 'error'
            })
            return;
        }

        let newPass = $form.find('input[name=new_pass]').val();
        if (!newPass) {
            $.toast({
                heading: 'Có lỗi xảy ra',
                text: 'Vui lòng nhập mật khẩu mới',
                position: 'bottom-right',
                icon: 'error'
            })
            return;
        }

        let renewPass = $form.find('input[name=renew_pass]').val();
        if (!renewPass) {
            $.toast({
                heading: 'Có lỗi xảy ra',
                text: 'Vui lòng nhập lại mật khẩu mới',
                position: 'bottom-right',
                icon: 'error'
            })
            return;
        }

        if (newPass !== renewPass) {
            $.toast({
                heading: 'Có lỗi xảy ra',
                text: 'Mật khẩu nhập lại không đúng',
                position: 'bottom-right',
                icon: 'error'
            })
            return;
        }

        if (oldPass === newPass) {
            $.toast({
                heading: 'Có lỗi xảy ra',
                text: 'Mật khẩu cũ và mật khẩu mới không được trùng nhau',
                position: 'bottom-right',
                icon: 'error'
            })
            return;
        }

        $('#' + formId + ' input').each(function() {
            formData.append($(this).attr("name"), $(this).val());
        });

        fetch($('#' + formId).data('action'), {
                method: $('#' + formId).data('method'),
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.result > 0) {
                    $.toast({
                        heading: 'Thành công',
                        text: 'Đổi mật khẩu thành công',
                        position: 'bottom-right',
                        icon: 'success'
                    });
                    $('input.require').val('');
                } else
                    $.toast({
                        heading: 'Có lỗi xảy ra',
                        text: data.msg,
                        position: 'bottom-right',
                        icon: 'error'
                    });
            })
            .catch(error => console.log(error.message));

    },

    submitFeeForm: function(formId, type) {
        let $form = $('#' + formId);
        let feeServiceArray = [];
        $form.find('.fee_body').children('.fee_item').each(function() {
            let $that = $(this);
            let feeItemArray = [];
            $that.find("input").each(function() {
                if ($(this).val())
                    feeItemArray.push($(this).val());
            });
            if (feeItemArray.length === 3)
                feeServiceArray.push(feeItemArray);
        });

        if (!feeServiceArray.length) {
            $.toast({
                heading: 'Có lỗi xảy ra',
                text: 'Không có bản ghi nào được xử lý',
                position: 'bottom-right',
                icon: 'error'
            });
            return;
        }

        let formData = new FormData();
        formData.append('csrf_token', $('input[name=csrf_token]').val());
        formData.append('type', type);
        formData.append('data', JSON.stringify(feeServiceArray));
        let isEdit = getUrlParam('type');
        if (isEdit)
            formData.append('is_edit', 1);
        fetch($form.data('action'), {
                method: $form.data('method'),
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.result > 0) {
                    $.toast({
                        heading: 'Thành công',
                        text: 'Cập nhật phí thành công',
                        position: 'bottom-right',
                        icon: 'success'
                    });
                    $('.fee_item_added').remove();
                    $('input').val('');
                } else
                    $.toast({
                        heading: 'Có lỗi xảy ra',
                        text: data.msg,
                        position: 'bottom-right',
                        icon: 'error'
                    });
            })
            .catch(error => console.log(error.message));

    },
    
    submitCurrencyForm(formId){
    	 let $form = $('#' + formId);
         let formData = new FormData();
         let source = $form.find('#source').val();
         if (!source) {
             $.toast({
                 heading: 'Có lỗi xảy ra',
                 text: 'Vui lòng nhập mã tiền nguồn',
                 position: 'bottom-right',
                 icon: 'error'
             })
             return;
         }
         let sourceName = $form.find('#source_name').val();
         if (!sourceName) {
             $.toast({
                 heading: 'Có lỗi xảy ra',
                 text: 'Vui lòng nhập tên tiền nguồn',
                 position: 'bottom-right',
                 icon: 'error'
             })
             return;
         }
         
         let destination = $form.find('#destination').val();
         if (!sourceName) {
             $.toast({
                 heading: 'Có lỗi xảy ra',
                 text: 'Vui lòng nhập mã tiền đích',
                 position: 'bottom-right',
                 icon: 'error'
             })
             return;
         }
         
         let destinationName = $form.find('#destination_name').val();
         if (!destinationName) {
             $.toast({
                 heading: 'Có lỗi xảy ra',
                 text: 'Vui lòng nhập tên tiền đích',
                 position: 'bottom-right',
                 icon: 'error'
             })
             return;
         }
         
         let rate =  $form.find('#rate').val();
         if (!rate) {
             $.toast({
                 heading: 'Có lỗi xảy ra',
                 text: 'Vui lòng nhập tỷ giá',
                 position: 'bottom-right',
                 icon: 'error'
             })
             return;
         }
         
         $('#' + formId + ' input').each(function() {
             formData.append($(this).attr("name"), $(this).val());
         });
         
         fetch($form.data('action'), {
             method: $form.data('method'),
             body: formData
         })
         .then(response => response.json())
         .then(data => {
             if (data.result > 0) {
                 $.toast({
                     heading: 'Thành công',
                     text: 'Cập nhật tỷ giá thành công',
                     position: 'bottom-right',
                     icon: 'success'
                 });
                 $('input.form-control').val('');
                 $('#modal-form').modal('hide');
             } else
                 $.toast({
                     heading: 'Có lỗi xảy ra',
                     text: data.msg,
                     position: 'bottom-right',
                     icon: 'error'
                 });
         })
         .catch(error => console.log(error.message));
         
    },
    
    submitDepositForm(formId){
    	let $form = $('#' + formId);
        let formData = new FormData();
        
        let depositRate = $form.find('#deposit_value').val();
        if (!depositRate) {
            $.toast({
                heading: 'Có lỗi xảy ra',
                text: 'Vui lòng nhập tỷ giá đặt cọc',
                position: 'bottom-right',
                icon: 'error'
            })
            return;
        }
        
        $('#' + formId + ' input').each(function() {
            formData.append($(this).attr("name"), $(this).val());
        });
        
        fetch($form.data('action'), {
            method: $form.data('method'),
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.result > 0) {
                $.toast({
                    heading: 'Thành công',
                    text: 'Cập nhật tỷ lệ cọc đơn hàng thành công',
                    position: 'bottom-right',
                    icon: 'success'
                });
                $('input.form-control').val('');
                $('#modal-form').modal('hide');
            } else
                $.toast({
                    heading: 'Có lỗi xảy ra',
                    text: data.msg,
                    position: 'bottom-right',
                    icon: 'error'
                });
        })
        .catch(error => console.log(error.message));
    },
    
    createOrder(formId){
    	let $form = $('#' + formId);
    	let formData = new FormData();
    	let arrayInputData = [];
    	var errorIndex = -1;
    	$(".order_item").each(function(i, obj) {
    		let $that = $(obj);
    		let index = i+1;
    		    		
    		let name = $that.find('.item_name').val();
    	    if(!name){
    	    	$.toast({
                    heading: 'Có lỗi xảy ra',
                    text: 'Vui lòng nhập tên sản phẩm',
                    position: 'bottom-right',
                    icon: 'error'
                });
    	    	errorIndex = i;
                return false;
    	    }
    		let link = $that.find('.item_link').val();
    		if(!link){
    	    	$.toast({
                    heading: 'Có lỗi xảy ra',
                    text: 'Vui lòng nhập link sản phẩm',
                    position: 'bottom-right',
                    icon: 'error'
                });
    	    	errorIndex = i;
                return false;
    	    }
    		let color = $that.find('.item_color').val();
    		if(!color){
    	    	$.toast({
                    heading: 'Có lỗi xảy ra',
                    text: 'Vui lòng nhập màu sắc sản phẩm',
                    position: 'bottom-right',
                    icon: 'error'
                });
    	    	errorIndex = i;
                return false;
    	    }
    		
    		let size = $that.find('.item_size').val();
    		
    		if(!size){
    	    	$.toast({
                    heading: 'Có lỗi xảy ra',
                    text: 'Vui lòng nhập kích thước sản phẩm',
                    position: 'bottom-right',
                    icon: 'error'
                });
    	    	errorIndex = i;
                return false;
    	    }
    		
    		let quantity = $that.find('.item_quantity').val();
    		
    		if(!quantity){
    	    	$.toast({
                    heading: 'Có lỗi xảy ra',
                    text: 'Vui lòng nhập số lượng sản phẩm',
                    position: 'bottom-right',
                    icon: 'error'
                });
    	    	errorIndex = i;
                return false;
    	    }
    		
    		let price = $that.find('.item_price').val();
    		
    		if(!price){
    	    	$.toast({
                    heading: 'Có lỗi xảy ra',
                    text: 'Vui lòng nhập giá sản phẩm',
                    position: 'bottom-right',
                    icon: 'error'
                });
    	    	errorIndex = i;
                return false;
    	    }
    		
    		let image = $that.find('.file_name').val();
    		if(!image){
    	    	$.toast({
                    heading: 'Có lỗi xảy ra',
                    text: 'Vui lòng nhập link ảnh hoặc upload ảnh sản phẩm',
                    position: 'bottom-right',
                    icon: 'error'
                });
    	    	errorIndex = i;
                return false;
    	    }
    		
    		let orderItem = {
        			name: name,
        			link: link,
        			color: color,
        			size: size,
        			quantity: quantity,
        			price: price,
        			image: image,
        			currency: $that.find('#currency').val(),
        			is_upload: false,
        			item_desc: $that.find('.item_desc').val()
        	};
    		let uploadImage = $that.find('.filestyle')[0].files[0];
    		if(uploadImage){
    			orderItem.is_upload = true;   			
    			let imgName = Math.random().toString(36).substr(2, 11);
    			orderItem.image = imgName;
    			formData.append(imgName, uploadImage);
    		}
    		else{
    			
    			if(!isValidURL(orderItem.image)){
    				$.toast({
                        heading: 'Có lỗi xảy ra',
                        text: 'Link ảnh sản phẩm không hợp lệ',
                        position: 'bottom-right',
                        icon: 'error'
                    });
    				errorIndex = i;
    				return false;
    			}
    		}
    		
    		arrayInputData.push(orderItem);
    	});
    	
    	if(errorIndex >= 0){
    		$form.find(".order_item").eq(errorIndex).find(".error-item").show();
    		return;
    	}
    	formData.append('order_data', JSON.stringify(arrayInputData));
    	formData.append('csrf_token',$form.find('input[name=csrf_token]').val());
    	$('#submit_form').prop('disabled',true);
    	$('input.form-control').prop('disabled', true);
    	$.ajax({
    	      url: "/dashboard/create-order",
    	      type: 'POST',
    	      processData: false, // important
    	      contentType: false, // important
    	      dataType : 'json',
    	      data: formData,
    	      success : function(data){
    	    	  if (data.result > 0) {
    	                $.toast({
    	                    heading: 'Thành công',
    	                    text: 'Tạo đơn hàng thành công',
    	                    position: 'bottom-right',
    	                    icon: 'success'
    	                });
    	               
    	            } else{
    	            	$('#submit_form').prop('disabled',false);
    	            	$.toast({
    	                    heading: 'Có lỗi xảy ra',
    	                    text: data.msg,
    	                    position: 'bottom-right',
    	                    icon: 'error'
    	                });
    	            }  	                
    	      },
    	 });
    },
    createUser(formId){
    	var $form = $('#' + formId);
    	var isError = false;
    	$form.find('input').each(function() {
            var value = $(this).val();
            var type = $(this).getType();         
            if ($(this).hasClass('require') && !value) {
                var msg = $(this).data('require');
                $.toast({
                    heading: 'Có lỗi xảy ra',
                    text: msg,
                    position: 'bottom-right',
                    icon: 'error'
                })
                isError = true;
                return false;
            }
        });
    	
    	if (!isError){
    		$('#submit_form').prop('disabled',true);
    		 $.ajax({
    	           type: $form.data('method'),
    	           url: $form.data('action'),
    	           data: $form.serialize(), // serializes the form's elements.
    	           success: function(data)
    	           {
    	        	   if (data.result > 0) {
	       	                $.toast({
	       	                    heading: 'Thành công',
	       	                    text: 'Tạo tài khoản thành công',
	       	                    position: 'bottom-right',
	       	                    icon: 'success'
	       	                });
       	                	$('input.require').val('');
	       	            } else{
	       	            	$('#submit_form').prop('disabled',false);
	       	            	$.toast({
	       	                    heading: 'Có lỗi xảy ra',
	       	                    text: data.msg,
	       	                    position: 'bottom-right',
	       	                    icon: 'error'
	       	                });
	       	            }
    	           }
    	      });
    	}          
    },
    confirmEditOrderDetail(t, id){
    	if(!$(t).siblings('.btn-danger').length){
    		$.toast({
                heading: 'Có lỗi xảy ra',
                text: 'Vui lòng edit sản phẩm trước khi thực hiện thao tác!',
                position: 'bottom-right',
                icon: 'error'
            });
    		return;
    	}
    		
    	
    	let formData = new FormData();
        formData.append('csrf_token', $('input[name=csrf_token]').val());
        var isError = false;
        $(t).parents('.order_item').find('table tbody tr td input').each(function(i) {
        	var value = $(this).val();
        	if(!value){
        		isError = true;
        		var fieldError = $(this).parents('tr').find('td').eq(0).text().toLowerCase();
        		$.toast({
                    heading: 'Có lỗi xảy ra',
                    text: 'Thông tin không được bỏ trống: ' + fieldError,
                    position: 'bottom-right',
                    icon: 'error'
                });
        		return false;
        	}
        	 formData.append($(this).attr("name"), $(this).val());
        });
        
        if(isError)
        	return;
        
        $(t).prop('disabled', true);
        fetch('/admin/update-order-detail', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.result > 0) {
                $.toast({
                    heading: 'Thành công',
                    text: 'Cập nhật sản phẩm thành công',
                    position: 'bottom-right',
                    icon: 'success'
                });
                $('input.require').val('');
            } else
                $.toast({
                    heading: 'Có lỗi xảy ra',
                    text: data.msg,
                    position: 'bottom-right',
                    icon: 'error'
                });
        })
        .catch(error => console.log(error.message));
        
    },
    
    confirmEditOrder(t, id){
    	if(!$(t).siblings('.btn-danger').length){
    		$.toast({
                heading: 'Có lỗi xảy ra',
                text: 'Vui lòng edit đơn hàng trước khi thực hiện thao tác!',
                position: 'bottom-right',
                icon: 'error'
            });
    		return;
    	}
    	let formData = new FormData();
        formData.append('csrf_token', $('input[name=csrf_token]').val());
        var $parentElm = $(t).parents('.order_footer');
        var status = $parentElm.find('#order_type').val();
        formData.append('status', status);
        formData.append('id', id);
        var userDeposit = $parentElm.find('input#user_deposit').val();
        if(userDeposit < 0){
        	$.toast({
                heading: 'Có lỗi xảy ra',
                text: 'Thông tin khách hàng cọc không hợp lệ',
                position: 'bottom-right',
                icon: 'error'
            });
    		return;
        }
        formData.append('user_deposit', userDeposit);
        
        var totalWeight = $parentElm.find('input#total_weight').val();
        if(totalWeight < 0){
        	$.toast({
                heading: 'Có lỗi xảy ra',
                text: 'Thông tin khối lượng hàng hóa không hợp lệ',
                position: 'bottom-right',
                icon: 'error'
            });
    		return;
        }
        formData.append('total_weight', totalWeight);
        
        var finalPrice = $parentElm.find('input#final_price').val();
        if(totalWeight < 0){
        	$.toast({
                heading: 'Có lỗi xảy ra',
                text: 'Thông tin tổng giá trị đơn hàng không hợp lệ',
                position: 'bottom-right',
                icon: 'error'
            });
    		return;
        }
        formData.append('final_price', finalPrice);
        $(t).prop('disabled', true);
        fetch('/admin/update-order', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.result > 0) {
                $.toast({
                    heading: 'Thành công',
                    text: 'Cập nhật đơn hàng thành công',
                    position: 'bottom-right',
                    icon: 'success'
                });
            } else
                $.toast({
                    heading: 'Có lỗi xảy ra',
                    text: data.msg,
                    position: 'bottom-right',
                    icon: 'error'
                });
        })
        .catch(error => console.log(error.message));
        
    },
    searchUser(t){
    	var $form = $(t).parents('form');
    	var email = $form.find('input#email').val();
    	if(!email){
    		$.toast({
                heading: 'Có lỗi xảy ra',
                text: 'Vui lòng nhập tài khoản cần tìm kiếm',
                position: 'bottom-right',
                icon: 'error'
            });
    		return;
    	}
    	
    	$.post($form.data('action'), {csrf_token: $('input[name=csrf_token]').val(),email : email.trim()}).done(function (data) {
            console.log(data);
            if(data.result > 0){
            	$form.find('#s_fullname').text(data.user.fullname);
                $form.find('#s_mobile').text(data.user.mobile);
                $form.find('#s_address').text(data.user.address);
                $form.find('#s_status').text(data.user.status ? 'Hoạt động':'Đã bị khóa');
                $form.find('#s_balance').text(formatMoney(data.user.balance) + 'đ');
                $form.find('#infomation').removeClass('hidden');
                return;
            }
            $form.find('#infomation').addClass('hidden');
            $.toast({
                heading: 'Có lỗi xảy ra',
                text: data.msg,
                position: 'bottom-right',
                icon: 'error'
            });
            
        });
    },
    topupUser: function(t){
    	var $form = $(t).parents('form');
    	var email = $form.find('input#email').val();
    	if(!email){
    		$.toast({
                heading: 'Có lỗi xảy ra',
                text: 'Vui lòng nhập tài khoản cần nạp tiền',
                position: 'bottom-right',
                icon: 'error'
            });
    		return;
    	}
    	
    	var total = $form.find('input#total').val();
    	if(!total){
    		$.toast({
                heading: 'Có lỗi xảy ra',
                text: 'Vui lòng nhập số tiền nạp',
                position: 'bottom-right',
                icon: 'error'
            });
    		return;
    	}
    	
    	$.ajax({
    		  url: $form.data('action'),
    		  type: 'PUT',
    		  data: {csrf_token: $('input[name=csrf_token]').val(),email : email.trim(), total: total},
    		  success: function(data) {
    			  if (data.result > 0) {
    	                $.toast({
    	                    heading: 'Thành công',
    	                    text: 'Nạp tiền thành công',
    	                    position: 'bottom-right',
    	                    icon: 'success'
    	                });
    	                $('input.form-control').val('');
    	            } else
    	                $.toast({
    	                    heading: 'Có lỗi xảy ra',
    	                    text: data.msg,
    	                    position: 'bottom-right',
    	                    icon: 'error'
    	                });
    		  }
    	});
    },
    userDeposit: function(){
    	var totalPriceFormat = formatMoney(total_price_wjlis);
    	var depositValue = Math.floor(total_price_wjlis * 70 / 100);
    	var depositValueFormat = formatMoney(depositValue);
    	$.confirm({
    	    title: 'Xác nhận đặt cọc!',
    	    content: `
    	    <div class="list-group no-radius alt">
				<a class="list-group-item" href="javascript:;"> <span class="badge bg-success">`+totalPriceFormat+`<sup>đ</sup></span>
					<i class="fa fa-money icon-muted"></i> Giá trị đơn hàng
				</a> <a class="list-group-item" href="javascript:;"> <span class="badge bg-info">`+depositValueFormat+`<sup>đ</sup></span>
					<i class="fa fa-truck icon-muted"></i> Bạn cần đặt cọc: (70% giá trị đơn)
				</a>
			</div>`,
    	    buttons: {
    	        confirm: function () {
    	            let balance = $('#user_balance').text().replace(/\D/g,'');
    	            if(balance < depositValue){
    	            	$.toast({
    	                    heading: 'Có lỗi xảy ra',
    	                    text: 'Số dư không đủ để thực hiện giao dịch',
    	                    position: 'bottom-right',
    	                    icon: 'error'
    	                });
    	            	return false;
	            	}
    	            else{
    	            	$.ajax({
	    	          		  url: "/dashboard/order-detail",
	    	          		  type: 'PUT',
	    	          		  data: {csrf_token: $('input[name=csrf_token]').val(), code: getUrlParam('code') },
	    	          		  success: function(data) {
	    	          			  if (data.result > 0) {
	    	          	                $.toast({
	    	          	                    heading: 'Thành công',
	    	          	                    text: 'Đặt cọc thành công',
	    	          	                    position: 'bottom-right',
	    	          	                    icon: 'success'
	    	          	                });
	    	          	                $('#bt_deposit_order').remove();
	    	          	              $('#user_balance').text('Loading...')
	    	          	                setTimeout(function(){ window.location.reload(); }, 3000);
	    	          	                
	    	          	            } else
	    	          	                $.toast({
	    	          	                    heading: 'Có lỗi xảy ra',
	    	          	                    text: data.msg,
	    	          	                    position: 'bottom-right',
	    	          	                    icon: 'error'
	    	          	                });
	    	          		  },
	    	          		  error: function (request, status, error) {
		    	          	        console.log(request.responseText);
			    	          	    $.toast({
	  	          	                    heading: 'Có lỗi xảy ra',
	  	          	                    text: 'Hệ thống đang bận, vui lòng thử lại sau',
	  	          	                    position: 'bottom-right',
	  	          	                    icon: 'error'
  	          	                	});
		    	          	  }
    	            	});
    	            }
    	        },
    	        cancel: function () {
    	        	text: 'Hủy'
    	        }
    	    }
    	});
    	    	
    },
    getOrderStatusText(status){
    	let text = "Không xác định";
    	switch (status) {
    	  case 0:
    	    text = "Khởi tạo";
    	    break;
    	  case 1:
    		  text = "Đã đặt cọc";
    	    break;
    	  case 2:
    		  text = "Đã đặt hàng";
    	    break;
    	  case 3:
    		  text = "Hàng về kho nước ngoài";
    	    break;
    	  case 4:
    		  text = "Đang ship về VN";
    	    break;
    	  case 5:
    		  text = "Đã tới kho VN";
    	    break;
    	  case 6:
    		  text = "Đang ship nội địa";
    		break;
    	  case 7:
    		  text = "Khách đã nhận";
    		break;
    	  case 8:
    		  text = "Nghi vấn";
    		break;
    	  case 9:
    		  text = "Bị hủy";
    		break;
    		  
    	}
    	return text;
    }
}


function rowspanDTable(oSettings, divId, time) { // time = 1 (theo giờ) = 0
    // theo ngày, sum = 1 (sum
    // dòng) = 0 ( bỏ sum )
    if (time == null || time == undefined || time == "") {
        time = -1;
    }
    if (oSettings.aiDisplay.length <= 0)
        return;
    $("#" + divId + " tbody tr td").removeAttr("hidden").removeAttr("rowspan");
    for (i = 0; i < oSettings.nTBody.childElementCount; i++) {
        for (j = 0; j < oSettings.nTBody.rows[i].childElementCount; j++) {
            var count = 1;
            var cellIndex = parseInt(oSettings.nTBody.rows[i].cells[j]._DT_CellIndex.column);
            if (oSettings.aoColumns[cellIndex].sType != "num" && oSettings.aoColumns[cellIndex].sType != "num-fmt") {
                if (oSettings.aoColumns[cellIndex].sType == "date") {
                    var strdate = oSettings.nTBody.rows[i].cells[j].textContent.toString().trim();
                    var n = strdate.indexOf("T");
                    if (n >= 0) {
                        if (n > 0) {
                            strdate = strdate.replace("T", " "); // replace
																	// time
                        } else {
                            strdate = strdate.replace("T", ""); // replace time
                        }
                        if (parseInt(time) == 0) { // ngày

                            var date = Utils.dateTypeFormatter(strdate, 0);
                            $('#' + divId + ' tbody tr:eq(' + i + ') td:eq(' + j + ')').text(date);
                        } else if (parseInt(time) == 2) {
                            var date = Utils.dateTypeFormatter(strdate, 2);
                            $('#' + divId + ' tbody tr:eq(' + i + ') td:eq(' + j + ')').text(date);
                        } else { // giờ
                            var date = Utils.dateTypeFormatter(strdate, 1);
                            $('#' + divId + ' tbody tr:eq(' + i + ') td:eq(' + j + ')').text(date);
                        }
                    }
                }
                if (i == 0) {
                    for (index = i + 1; index < oSettings.nTBody.childElementCount; index++) {
                        var strdate = oSettings.nTBody.rows[index].cells[j].textContent.toString();
                        if (oSettings.aoColumns[cellIndex].sType == "date") {
                            var n = strdate.indexOf("T");
                            if (n >= 0) {
                                strdate = strdate.replace("T", " "); // replace
                                // time
                                if (parseInt(time) == 0) {
                                    strdate = Utils.dateTypeFormatter(strdate, 0);
                                    // $('#' + divId + ' tbody tr:eq(' + i + ')
                                    // td:eq(' + j + ')').text(date);
                                } else if (parseInt(time) == 2) {
                                    strdate = Utils.dateTypeFormatter(strdate, 2);
                                } else {
                                    strdate = Utils.dateTypeFormatter(strdate, 1);
                                    // $('#' + divId + ' tbody tr:eq(' + i + ')
                                    // td:eq(' + j + ')').text(date);
                                }
                            }
                        }
                        if (oSettings.nTBody.rows[i].cells[j].textContent != strdate)
                            break;
                        count++;
                    }
                    if (count > 1) {
                        $('#' + divId + ' tbody tr:eq(' + i + ') td:eq(' + j + ')').attr("rowspan", count);
                    }
                } else {
                    if (oSettings.nTBody.rows[i - 1].cells[j].textContent == oSettings.nTBody.rows[i].cells[j].textContent)
                        $('#' + divId + ' tbody tr:eq(' + i + ') td:eq(' + j + ')').attr("hidden", "true");
                    else {
                        for (index = i + 1; index < oSettings.nTBody.childElementCount; index++) {
                            var strdate = oSettings.nTBody.rows[index].cells[j].textContent.toString();
                            if (oSettings.aoColumns[cellIndex].sType == "date") {
                                var n = strdate.indexOf("T");
                                if (n >= 0) {
                                    strdate = strdate.replace("T", " "); // replace
                                    // time
                                    if (parseInt(time) == 0) {
                                        strdate = Utils.dateTypeFormatter(strdate, 0);
                                        // $('#' + divId + ' tbody tr:eq(' + i +
                                        // ') td:eq(' + j + ')').text(date);
                                    } else if (parseInt(time) == 2) {
                                        strdate = Utils.dateTypeFormatter(strdate, 2);
                                    } else {
                                        strdate = Utils.dateTypeFormatter(strdate, 1);
                                        // $('#' + divId + ' tbody tr:eq(' + i +
                                        // ') td:eq(' + j + ')').text(date);
                                    }
                                }
                            }
                            if (oSettings.nTBody.rows[i].cells[j].textContent != strdate)
                                break;
                            count++;
                        }
                        if (count > 1) {
                            $('#' + divId + ' tbody tr:eq(' + i + ') td:eq(' + j + ')').attr("rowspan", count);
                        }
                    }
                }
            } else {
                var number = oSettings.nTBody.rows[i].cells[j].textContent.toString();
                if (number != "" && number != null) {
                    var n = number.indexOf(" ");
                    if (n < 0) {
                        number = formatMoney(number);
                        $('#' + divId + ' tbody tr:eq(' + i + ') td:eq(' + j + ')').css("text-align", "right").text(number);
                    } else {
                        $('#' + divId + ' tbody tr:eq(' + i + ') td:eq(' + j + ')').text(number);
                    }
                }
            }
        }

    }
}

function formatMoney(argValue) {
    if (argValue == null || argValue == "")
        return argValue;

    var str1 = argValue.toString();
    if (str1.indexOf(",") >= 0 || str1.indexOf(".") >= 0)
        str1 = argValue.replace(/[,.]/g, "");

    argValue = parseInt(str1);
    var _comma = (1 / 2 + '').charAt(1);
    var _digit = ',';
    if (_comma == '.') {
        _digit = '.';
    }

    var _sSign = "";
    if (argValue < 0) {
        _sSign = "-";
        argValue = -argValue;
    }

    var _sTemp = "" + argValue;
    var _index = _sTemp.indexOf(_comma);
    var _digitExt = "";
    if (_index != -1) {
        _digitExt = _sTemp.substring(_index + 1);
        _sTemp = _sTemp.substring(0, _index);
    }

    var _sReturn = "";
    while (_sTemp.length > 3) {
        _sReturn = _digit + _sTemp.substring(_sTemp.length - 3) + _sReturn;
        _sTemp = _sTemp.substring(0, _sTemp.length - 3);
    }
    _sReturn = _sSign + _sTemp + _sReturn;
    if (_digitExt.length > 0) {
        _sReturn += _comma + _digitExt;
    }
    return _sReturn;
}

function getUrlParam(param) {
    return new URL(window.location.href).searchParams.get(param);
}

function isValidURL(string) {
	  var res = string.match(/(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g);
	  return (res !== null)
};