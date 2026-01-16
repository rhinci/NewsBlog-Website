from django.shortcuts import render, redirect
import datetime
from django.http import Http404
from django import forms
from .forms import ContactForm
from .forms import ArticleForm
from .forms import CommentForm
from .forms import RegisterForm
from .forms import LoginForm
from django.contrib import messages
from .models import Article
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


# ARTICLES = [
#     {'id': 1, 'title': 'Фараонова пирамида памяти', 'content': 'Коричневое ухо фараонов, китовых борозд на грифах оснащения НЛО с подоплекой зрелости вправленного закатившегося ирокеза аккомпанементов метеоритов с призмой хип-хопа в гладком инструменте минимума каверзных животных мира, относясь к морям галактики для прояснения педалей слез. Как первая крепкая планета шествования с остатком объема строгого превращения пирамиды в излучатель системы гениальной головы лечения больных людей. Как огромнейшая потуга заутюженного солнцем стебля для огромного пресса обводки лица, отгравированного плауна, мягкой логики распространения среди людей правдивых управлений стежками, троекратного корня компьютера в превышенном шлейфе стройки логики, как связь звезд и доброты в сжатом кулаке, обоюдности простоты с перебитым штатом бессмертия. Как впрягающаяся верховность правления комка, просчитанного в прошлом времени и во всем времени галактики, двигателя сердца - главного снижателя эмоций в сторону рассудительного плача. Как раскрытая идентичность любви. Как слитая земля программой НЛО для адекватности управления головой. Затягивали тень человека в теплую полость рубящих камней психики для удержания от слез относительно фараонов. Чтобы добротная рассеяность живучести толкалки зарисованной логики рубикона ярко-выраженных вкраплений мяса. На коротящих усыпальницах, раскрашенной фараонской божественной отвественности пирамид, было щенком тонкого шествования по земле. Как наша планета, стоящая на месте с уступкой главы мечты для всеобъемлющих планет памяти слез.', 'date': datetime.date.today()},
#     {'id': 2, 'title': 'Идущий к реке', 'content':'Я в своем познании настолько преисполнился, что я как будто бы уже сто триллионов миллиардов лет проживаю на триллионах и триллионах таких же планет, как эта Земля, мне этот мир абсолютно понятен, и я здесь ищу только одного - покоя, умиротворения и вот этой гармонии, от слияния с бесконечно вечным, от созерцания великого фрактального подобия и от вот этого замечательного всеединства существа, бесконечно вечного, куда ни посмотри, хоть вглубь - бесконечно малое, хоть ввысь - бесконечное большое, понимаешь? А ты мне опять со своим вот этим, иди суетись дальше, это твоё распределение, это твой путь и твой горизонт познания и ощущения твоей природы, он несоизмеримо мелок по сравнению с моим, понимаешь? Я как будто бы уже давно глубокий старец, бессмертный, ну или там уже почти бессмертный, который на этой планете от её самого зарождения, ещё когда только Солнце только-только сформировалось как звезда, и вот это газопылевое облако, вот, после взрыва, Солнца, когда оно вспыхнуло, как звезда, начало формировать вот эти коацерваты, планеты, понимаешь, я на этой Земле уже как будто почти пять миллиардов лет живу и знаю её вдоль и поперёк этот весь мир, а ты мне какие-то... мне не важно на твои тачки, на твои яхты, на твои квартиры, там, на твоё благо. Я был на этой планете бесконечным множеством, и круче Цезаря, и круче Гитлера, и круче всех великих, понимаешь, был, а где-то был конченым говном, ещё хуже, чем здесь. Я множество этих состояний чувствую. Где-то я был больше подобен растению, где-то я больше был подобен птице, там, червю, где-то был просто сгусток камня, это всё есть душа, понимаешь? Она имеет грани подобия совершенно многообразные, бесконечное множество. Но тебе этого не понять, поэтому ты езжай себе, мы в этом мире как бы живем разными ощущениями и разными стремлениями, соответственно, разное наше и место, разное и наше распределение. Тебе я желаю все самые крутые тачки чтоб были у тебя, и все самые лучше самки, если мало идей, обращайся ко мне, я тебе на каждую твою идею предложу сотню триллионов, как всё делать. Ну а я всё, я иду как глубокий старец, узревший вечное, прикоснувшийся к Божественному, сам стал богоподобен и устремлен в это бесконечное, и который в умиротворении, покое, гармонии, благодати, в этом сокровенном блаженстве пребывает, вовлеченный во всё и во вся, понимаешь, вот и всё, в этом наша разница. Так что я иду любоваться мирозданием, а ты идёшь преисполняться в ГРАНЯХ каких-то, вот и вся разница, понимаешь, ты не зришь это вечное бесконечное, оно тебе не нужно. Ну зато ты, так сказать, более активен, как вот этот дятел долбящий, или муравей, который очень активен в своей стезе, поэтому давай, наши пути здесь, конечно, имеют грани подобия, потому что всё едино, но я-то тебя прекрасно понимаю, а вот ты меня - вряд ли, потому что я как бы тебя в себе содержу, всю твою природу, она составляет одну маленькую там песчиночку, от того что есть во мне, вот и всё, поэтому давай, ступай, езжай, а я пошел наслаждаться прекрасным осенним закатом на берегу теплой южной реки. Всё, ступай, и я пойду.', 'date': datetime.date.today()},
#     {'id': 3, 'title': 'Диалог о вере и тишине', 'content': 'Один умный профессор однажды в университете задал студенту интересный вопрос. \nПрофессор: Бог хороший?\n Студент: Фыр.\nПрофессор: А Дьявол хороший?\nСтудент: Шкшкшк.\nПрофессор: Верно. Скажи мне, сынок, существует ли на Земле зло?\nСтудент: Фыр.\nПрофессор: Зло повсюду, не так ли? И Бог создал все, верно?\nСтудент: Фыр.\nПрофессор: Так кто создал зло?\nСтудент: Ихихих.\nПрофессор: На планете есть уродство, наглость, болезни, невежество? Все это есть, верно?\nСтудент: Фыр фыр.\nПрофессор: Так кто их создал?\nСтудент: Ихихих.\nПрофессор: Наука утверждает, что у человека есть 5 чувств, чтобы исследовать мир вокруг. Скажи мне, сынок, ты когда-нибудь видел Бога?\nСтудент: Шкшкшкшкшк.\nПрофессор: Скажи нам, ты слышал Бога?\nСтудент: Шкшкшкшкшк.\nПрофессор: Ты когда-нибудь ощущал Бога? Пробовал его на вкус? Нюхал его?\nСтудент: Ихихих, шкшкшкшк.\nПрофессор: И ты до сих пор в него веришь?\nСтудент: Фыр.\nПрофессор: Исходя из полученных выводов, наука может утверждать, что Бога нет. Ты можешь что-то противопоставить этому?\nСтудент: Шкшкшк. Ихихихих фыр фыр фыр.\nПрофессор: Вот именно. Вера – это главная проблема науки.\nСтудент: Фыр фыр, ихихихихих?\nПрофессор: Что за вопрос? Конечно, существует. Тебе никогда не было холодно? (Студенты засмеялись над вопросом молодого человека)\nСтудент: Ихихихихих, фыр фыр фыр фыр. Шкшкшкшкшк, фыр фыр фыр ихихихихих. Ихихихихих фыр фыр ихихихихих. Фыр фыр ихихих, фыр фыр фыр. Ихихихихих, ихихихих шкшкшкшкшкшк. Фыр, ихих, фыр фыр фыр фыр, ихихихихих. Фыр фыр фыр фыр фыр. (В аудитории повисла тишина)\nСтудент: Ихих, фыр фыр фыр?\nПрофессор: Конечно, существует. Что такое ночь, если не темнота.\nСтудент: Ихихихихих фыр фыр ихихихихих. Шкшкшкшкшк, ихихихих фыр фыр фыр, ихихих. Фыр фыр, шкшкшкшкшкш, фыр ихихихихих. Фыр фыр ихихих, фыр фыр фыр. Ихихихихих, ихихихих шкшкшкшкшкшк. Фыр фыр фыр ихихих.\nПрофессор: Конечно. Есть жизнь, и есть смерть – обратная ее сторона.\nСтудент: Ихихихих шкшкшкшкшк фыр фыр фыр. Ихихих, фыр фыр шкшк фыр фыр фыр. Фыр ихихих.\nПрофессор: К чему вы ведете, молодой человек?\nСтудент: Ихихих, фыр фыр фыр шкшк фыр фыр. Фыр ихих фыр фыр шкшкшк.\nПрофессор покачал головой с улыбкой, понимая, к чему идет разговор.\nСтудент: Фыр фыр фыр, ихихихихих фыр фыр. Шкшкшкшк, фыр фыр фыр. Ихих фыр фыр. (Аудитория взорвалась от смеха)\nСтудент: Ихихих, фыр фыр фыр шкшк ихих фыр фыр? Ихих фыр фыр ихихихих шкшкшк фыр? (Студенты продолжали смеяться)\nСтудент: Шкшкшк. Ихихих, фыр фыр шк фыр фыр. Ихихих, фыр фыр шкшкшкшкш, фыр фыр ихихих? (В аудитории повисла тишина)\nПрофессор: Думаю, вам просто стоит мне поверить.\nСтудент: Фыр фыр! Ихихих, фыр фыр фыр фыр шкшкшкшк фыр!\nПрофессор сел\nЭтим студентом была огромная ехидна.', 'date': datetime.date(2025, 1, 1)}

# ]

def index(request):
    today = datetime.date.today()

    category = request.GET.get('category', '')

    if category:
        articles_list = Article.objects.filter(category=category).order_by('-created_date')
    else:
        articles_list = Article.objects.all().order_by('-created_date')

    articles = []
    for article in articles_list:
        is_new = article.created_date.date() == today
        articles.append({
            'object': article,
            'is_new': is_new
        })

    categories = Article.CATEGORY_CHOICES
    
    context = {
        'articles': articles,
        'categories': categories,
        'current_category': category
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'blog/about.html')

def contacts(request):
    return render(request, 'blog/contacts.html')

def feedback(request):
    context = {}
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message_text = form.cleaned_data['message']

            messages.success(request, "Спасибо! Сообщение отправлено.")
            return redirect('feedback')
    else:
        form = ContactForm()
    return render(request, 'blog/feedback.html', {'form': form})


def news(request, id):
    article = get_object_or_404(Article, id=id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            return redirect('news', id=article.id)
    else:
        form = CommentForm()

    comments = article.comments.all().order_by('-date')
    
    context = {
        'article': article,
        'form': form,
        'comments': comments
    }
    return render(request, 'blog/news.html', context)

@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('index')
    else:
        form = ArticleForm()
    
    return render(request, 'blog/create_article.html', {'form': form})

@login_required
def edit_article(request, id):
    article = get_object_or_404(Article, id=id)

    if article.user != request.user:
        messages.error(request, "Вы можете редактировать только свои статьи")
        return redirect('index')
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('news', id=article.id)
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'blog/edit_article.html', {
        'form': form, 
        'article': article
    })

@login_required
def delete_article(request, id):
    article = get_object_or_404(Article, id=id)

    if article.user != request.user:
        messages.error(request, "Вы можете удалять только свои статьи")
        return redirect('index')

    article.delete()
    messages.success(request, "Статья успешно удалена")
    return redirect('index')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = LoginForm()
    
    return render(request, 'blog/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')