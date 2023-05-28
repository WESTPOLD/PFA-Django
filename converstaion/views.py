from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from Product.models import Item
from converstaion.forms import ConversationMessageForm
from converstaion.models import Conversation 
# Create your views here.
@login_required
def new_conversation(request,item_pk):
    item = get_object_or_404(Item,pk=item_pk)

    if item.creatd_by == request.user:
        return redirect("dashboard:index")
    
    conversations =  Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    # if conversations:
    #     return redirect('conversation:detail', pk=conversations.first().id)
    
    if request.method == "POST":
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.creatd_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()
            
            return redirect('Product:detail',pk=item_pk)
    else:
        form  = ConversationMessageForm()

    return render(request,'conversation/new.html',{
        'form':form,
    })
            
@login_required
def inbox(request):
    conversations =  Conversation.objects.filter(members__in=[request.user.id])
    return render(request,'conversation/inbox.html',{
        'conversations':conversations
    })