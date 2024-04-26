# import json
# from django.contrib.auth.decorators import login_required
# from django.http import Http404, HttpResponse
# from walletapp.TransactionException import TransferException
# from .forms import BankAccForm, SearchUserForm, RequestForm, SendForm
# from django.shortcuts import render
# from payapp.core.banking.bank import get_user_bank_acc, delete_bank_acc, get_acc_id
# from popup.popup import PopupHttpResponse
# from popup.views import no_view
# from payapp.core.banking.search import search_by_id
# from payapp.core.banking.transfers import add_transfer_req, withdraw_trans_req, approve_trans_req, deny_trans_req, transfer_money
#
#
# @login_required(login_url='login')
# def index(request):
#     notifications = fetch_user_notifications(request.user.id)
#     return render(request, 'payapp/banking/layout/index.html', {'count': len(notifications)})
#
#
# def create_bank_acc(request):
#     form = BankAccForm()
#
#     if request.method == 'POST':
#         form = BankAccForm(request.POST)
#         if form.is_valid():
#             account = form.save(request.user)
#             return PopupHttpResponse(success=True, title='New Bank Account Added',
#                                      message=f'{account.bank_name} has been added to your account.')
#     return render(request, 'payapp/banking/modal/create-account.html', {'form': form})
#
#
# def list_bank_acc(request):
#     if not request.method == 'GET':
#         return PopupHttpResponse(success=False, title='Error Occurred', message='Not Allowed')
#
#     user_id = request.GET.get('user_id')
#     if not user_id:
#         return PopupHttpResponse(success=False, title='Error Occurred', message='Not Allowed')
#
#     accounts = get_user_bank_acc(user_id)
#     if len(accounts) <= 0:
#         return no_view(request, 'No Accounts Added', 'You have not added any accounts yet.')
#
#     context = {
#         'accounts': accounts
#     }
#     return render(request, 'payapp/banking/modal/list-accounts.html', context)
#
#
# def remove_bank_acc(request):
#     if request.method == 'POST':
#         id = request.POST.get('id')
#         delete_bank_acc(id)
#         return PopupHttpResponse(success=True, title='Bank Account Removed',
#                                  message='Bank account has been successfully removed from your account')
#
#     context = {
#         'account': get_acc_id(account_id=request.GET.get('id'))
#     }
#     return render(request, 'payapp/banking/modal/confirm-remove.html', context)
#
#
# @login_required(login_url='login')
# def transfer_requests(request):
#     notifications = fetch_user_notifications(request.user.id)
#     if request.method == 'GET':
#         return render(request, 'payapp/banking/layout/tr-requests.html', {'count': len(notifications)})
#     raise Http404()
#
#
# @login_required(login_url='login')
# def list_transfer_requests(request):
#     if request.method == 'GET':
#         group = request.GET.get('group') if request.GET.get(
#             'group') is not None else 'all'
#         results = add_transfer_req(request.user.id, group)
#         context = {
#             'transfer_requests': results,
#             'group': group,
#             'count': len(results)
#         }
#         print(len(results))
#         return render(request, 'payapp/banking/modal/list-transfer-requests.html', context)
#     return HttpResponse('No content')
#
#
# @login_required(login_url='login')
# def confirm_transfer_withdrawal(request):
#     if request.method == 'GET':
#         context = {
#             'rid': request.GET.get('rid')
#         }
#         return render(request, 'payapp/banking/modal/withdraw-confirm.html', context)
#     return HttpResponse('No content')
#
#
# @login_required(login_url='login')
# def confirm_transfer_approval(request):
#     if request.method == 'GET':
#         context = {
#             'tr': add_transfer_req(request.GET.get('rid'))
#         }
#         return render(request, 'payapp/banking/modal/approval-confirm.html', context)
#     return HttpResponse('No content')
#
#
# @login_required(login_url='login')
# def confirm_transfer_denial(request):
#     if request.method == 'GET':
#         context = {
#             'tr': add_transfer_req(request.GET.get('rid'))
#         }
#         return render(request, 'payapp/banking/modal/denial-confirm.html', context)
#     return HttpResponse('No content')
#
#
# @login_required(login_url='login')
# def request_withdrawal(request):
#     if request.method == 'GET':
#         rid = request.GET.get('rid')
#         tr_rq = add_transfer_req(rid)
#         withdraw_trans_req(rid)
#         return PopupHttpResponse(True, 'Request Withdrawn',
#                                  f'Transfer request of {tr_rq.currency} {tr_rq.amount} was successfully withdrawn')
#
#     return HttpResponse('No content')
#
#
# @login_required(login_url='login')
# def approve_transfer(request):
#     if request.method == 'GET':
#         try:
#             rid = request.GET.get('rid')
#             tr_rq = add_transfer_req(rid)
#             approve_trans_req(rid)
#             return PopupHttpResponse(True, 'Money Transferred',
#                                      f'You have successfully transferred {tr_rq.amount} {tr_rq.currency} to {tr_rq.recipient.first_name}.')
#         except TransferException as te:
#             context = {
#                 'message': te.message
#             }
#             return render(request, 'payapp/banking/modal/send-failure.html', context)
#         except Exception as e:
#             return HttpResponse(f'Transaction Failed: {str(e)}')
#
#     return HttpResponse('No content')
#
#
# @login_required(login_url='login')
# def deny_transfer(request):
#     if request.method == 'GET':
#         try:
#             rid = request.GET.get('rid')
#             tr_rq = add_transfer_req(rid)
#             deny_trans_req(rid)
#             return PopupHttpResponse(True, 'Transfer Request Declined',
#                                      f'You have declined the transfer request from {tr_rq.recipient.first_name} for an amount of {tr_rq.currency} {tr_rq.amount} successfully')
#         except TransferException as te:
#             context = {
#                 'message': te.message
#             }
#             return render(request, 'payapp/banking/modal/send-failure.html', context)
#         except Exception as e:
#             return PopupHttpResponse(False, 'Error Occurred', f'{str(e)}')
#
#     return HttpResponse('No content')
#
#
# @login_required(login_url='login')
# def send_money(request):
#     notifications = fetch_user_notifications(request.user.id)
#     form = SearchUserForm()
#     results = []
#     if request.method == 'GET':
#         if 'identifier' in request.GET:
#             form = SearchUserForm(request.GET)
#
#         if form.is_valid():
#             results = form.search()
#
#         return render(request, 'payapp/banking/layout/send-money.html',
#                       {'form': form, 'search_results': results, 'count': len(notifications)})
#     else:
#         raise Http404()
#
#
# @login_required(login_url='login')
# def send_money_details(request):
#     print(f'user: {request.user}')
#     if request.method == 'POST' and 'confirm' not in request.POST:
#         receiver = get_acc_id(request.POST.get('receiver'))
#         form = SendForm(request.user.id, request.POST)
#         if form.is_valid():
#             context = {
#                 'form': form,
#                 'receiver': receiver,
#                 'sender': request.user,
#                 'amount': request.POST.get('amount'),
#                 'currency': request.POST.get('currency')
#             }
#             return render(request, 'payapp/banking/modal/send-money-confirm.html', context)
#         context = {
#             'form': form,
#             'receiver': receiver
#         }
#         return render(request, 'payapp/banking/modal/send-money-details.html', context)
#
#     elif request.method == 'POST' and 'confirm' in request.POST:
#
#         try:
#             sender_id = request.POST.get('sender')
#             receiver_id = request.POST.get('receiver')
#             amount = request.POST.get('amount')
#             currency = request.POST.get('currency')
#             receiver = get_acc_id(receiver_id)
#             transfer_money(sender_id, receiver_id, amount, currency)
#             return HttpResponse(status=204, headers={
#                 'HX-Trigger': json.dumps({
#                     'toast': {
#                         'success': True,
#                         'title': 'Money Transferred',
#                         'message': f'You have successfully transferred {amount} {currency} to {receiver.first_name}.'
#                     }
#                 })
#             })
#
#         except TransferException as te:
#             context = {
#                 'message': te.message
#             }
#             return render(request, 'payapp/banking/modal/send-money-failure.html', context)
#         except Exception as e:
#             return HttpResponse(f'Transaction Failed: {str(e)}')
#
#     elif 'recipient' not in request.GET:
#         raise Http404()
#     receiver = get_acc_id(request.GET.get('receiver'))
#     context = {
#         'form': SendForm(request.user.id),
#         'receiver': receiver
#     }
#     return render(request, 'payapp/banking/modal/send-money-details.html', context)
#
#
# @login_required(login_url='login')
# def request_money(request):
#     notifications = fetch_user_notifications(request.user.id)
#     form = SearchUserForm()
#     results = []
#     if request.method == 'GET':
#         if 'identifier' in request.GET:
#             form = SearchUserForm(request.GET)
#
#         if form.is_valid():
#             results = form.search()
#
#         return render(request, 'payapp/banking/layout/request-money.html',
#                       {'form': form, 'search_results': results, 'count': len(notifications)})
#     else:
#         raise Http404()
#
#
# @login_required(login_url='login')
# def request_money_details(request):
#     print(f'user: {request.user}')
#     if request.method == 'POST' and 'confirm' not in request.POST:
#         receiver = get_acc_id(request.POST.get('receiver'))
#         form = RequestForm(request.user.id, request.POST)
#         if form.is_valid():
#             context = {
#                 'form': form,
#                 'receiver': receiver,
#                 'sender': request.user,
#                 'amount': request.POST.get('amount'),
#                 'currency': request.POST.get('currency')
#             }
#             return render(request, 'payapp/banking/modal/request-money-confirm.html', context)
#         context = {
#             'form': form,
#             'receiver': receiver
#         }
#         return render(request, 'payapp/banking/modal/request-money-details.html', context)
#
#     elif request.method == 'POST' and 'confirm' in request.POST:
#
#         try:
#             sender_id = request.POST.get('sender')
#             receiver_id = request.POST.get('receiver')
#             amount = request.POST.get('amount')
#             currency = request.POST.get('currency')
#             add_transfer_req(sender_id, receiver_id, amount, currency)
#             context = {
#                 'form': RequestForm(request.user.id, request.POST),
#                 'receiver': search_by_id(receiver_id),
#                 'sender': request.user,
#                 'amount': amount,
#                 'currency': currency
#             }
#             return render(request, 'payapp/banking/modal/request-money-success.html', context)
#         except TransferException as te:
#             context = {
#                 'message': te.message
#             }
#             return render(request, 'payapp/banking/modal/request-money-failure.html', context)
#         except Exception as e:
#             return HttpResponse(f'Transaction Failed: {str(e)}')
#
#     elif 'receiver' not in request.GET:
#         raise Http404()
#     receiver = get_acc_id(request.GET.get('receiver'))
#     context = {
#         'form': RequestForm(request.user.id),
#         'receiver': receiver
#     }
#     return render(request, 'payapp/banking/modal/request-money-details.html', context)