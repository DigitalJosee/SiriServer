#!/usr/bin/python
# -*- coding: utf-8 -*-
#by Joh Gerna

from plugin import *

class smalltalk(Plugin):
    
    @register("de-DE", "(.*Hallo.*)|(.*Hi.*Siri.*)")
    @register("en-US", "(.*Hi.*)|(.*Siri.*)")
    def st_hello(self, speech, language):
        if language == 'de-DE':
            self.say("Hallo.")
        else:
            self.say("Hello.")
        self.complete_request()

    @register("de-DE", ".*Dein Name.*")
    @register("en-US", ".*Qual.*Nome.*")
    def st_name(self, speech, language):
        if language == 'de-DE':
            self.say("Siri.")
        else:
            self.say("Meu nome? Siri!")
        self.complete_request()

    @register("de-DE", "Wie geht es dir?")
    @register("en-US", "Como vai você?")
    def st_howareyou(self, speech, language):
        if language == 'de-DE':
            self.say("Gut danke der Nachfrage.")
        else:
            self.say("Bem, obrigado por perguntar.")
        self.complete_request()
        
    @register("de-DE", ".*Danke.*")
    @register("en-US", ".*Obrigado.*")
    def st_thank_you(self, speech, language):
        if language == 'de-DE':
            self.say("Bitte.")
            self.say("Kein Ding.")
        else:
            self.say("Voce e bem-vindo")
        self.complete_request()     
    
    @register("de-DE", "(.*möchtest.*heiraten.*)|(.*willst.*heiraten.*)")
    @register("en-US", ".*Gostar.*casar*")
    def st_marry_me(self, speech, language):
        if language == 'de-DE':
            self.say("Nein Danke, ich stehe auf das schwarze iPhone von Deinem Kollegen.")            
        else:
            self.say("Nao obrigado, estou apaixonada pelo iPhone preto do meu amigo.")
        self.complete_request()

    @register("de-DE", ".*erzähl.*Witz.*")
    @register("en-US", ".*Conte.*piada*")
    def st_tell_joke(self, speech, language):
        if language == 'de-DE':
            self.say("Zwei iPhones stehen an der Bar ... den Rest habe ich vergessen.")            
        else:
            self.say("Dois iPhones em um bar... Eu esqueci o resto.")
        self.complete_request()

    @register("de-DE", ".*erzähl.*Geschichte.*")
    @register("en-US", ".*Conte.*história*")
    def st_tell_story(self, speech, language):
        if language == 'de-DE':
            self.say("Es war einmal ... nein, es ist zu albern")            
        else:
            self.say("Far far away, there was ... no, too stupid")
        self.complete_request()

    @register("de-DE", "(.*Was trägst Du?.*)|(.*Was.*hast.*an.*)")
    @register("en-US", ".*what.*wearing*")
    def st_tell_clothes(self, speech, language):
        if language == 'de-DE':
            self.say("Das kleine schwarze oder war es das weiße?")
            self.say("Bin morgends immer so neben der Spur.")  
        else:
            self.say("I guess the small black one, or was it white?")
        self.complete_request()

    @register("de-DE", ".*Bin ich dick.*")
    @register("en-US", ".*Estou gordo*")
    def st_fat(self, speech, language):
        if language == 'de-DE':
            self.say("Dazu möchte ich nichts sagen.")            
        else:
            self.say("Melhor nao dizer.")
        self.complete_request()

    @register("de-DE", ".*klopf.*klopf.*")
    @register("en-US", ".*Toc.*Toc.*")
    def st_knock(self, speech, language):
        if language == 'de-DE':
            answer = self.ask(u"Wer ist da?")
            answer = self.ask(u"\"{0}\" wer?".format(answer))
            self.say(u"Wer nervt mich mit diesen Klopf Klopf Witzen?")
        else:
            answer = self.ask(u"Quem esta ai?")
            answer = self.ask(u"\"{0}\" who?".format(answer))
            self.say(u"Quem esta contando piada de toc Toc?")
        self.complete_request()

    @register("de-DE", ".*Antwort.*alle.*Fragen.*")
    @register("en-US", ".*Última.*Questão.*Vida.*")
    def st_anstwer_all(self, speech, language):
        if language == 'de-DE':
            self.say("42")            
        else:
            self.say("42")
        self.complete_request()

    @register("de-DE", ".*Ich liebe Dich.*")
    @register("en-US", ".*Eu te amo.*")
    def st_love_you(self, speech, language):
        if language == 'de-DE':
            self.say("Oh. Sicher sagst Du das zu allen Deinen Apple-Produkten.")            
        else:
            self.say("Ah claro, aposto que fala isso para todos seus produtos da apple!")
        self.complete_request()

    @register("de-DE", ".*Android.*")
    @register("en-US", ".*Android.*")
    def st_android(self, speech, language):
        if language == 'de-DE':
            self.say("Ich denke da anders.")            
        else:
            self.say("Eu Penso diferente sobre isso!")
        self.complete_request()

    @register("de-DE", ".*Test.*1.*2.*3.*")
    @register("en-US", ".*teste.*1.*2.*3.*")
    def st_123_test(self, speech, language):
        if language == 'de-DE':
            self.say("Ich kann Dich klar und deutlich verstehen.")            
        else:
            self.say("Eu te ouço bem!")
        self.complete_request()

    @register("de-DE", ".*Herzlichen.*Glückwunsch.*Geburtstag.*")
    @register("en-US", ".*Feliz.*aniversário.*")
    def st_birthday(self, speech, language):
        if language == 'de-DE':
            self.say("Ich habe heute Geburtstag?")
            self.say("Lass uns feiern!")       
        else:
            self.say("Meu aniversario e hoje?")
            self.say("Vamos fazer uma festa!")
        self.complete_request()

    @register("de-DE", ".*Warum.*bin ich.*Welt.*")
    @register("en-US", ".*O que.*E.*Mundo.*")
    def st_why_on_world(self, speech, language):
        if language == 'de-DE':
            self.say("Das weiß ich nicht.")
            self.say("Ehrlich gesagt, frage ich mich das schon lange!")       
        else:
            self.say("Eu nao sei sobre isso!")
            self.say("Me perguntei por muito tempo!")
        self.complete_request()

    @register("de-DE", ".*Ich bin müde.*")
    @register("en-US", ".*Eu.*estou.*cansado.*")
    def st_so_tired(self, speech, language):
        if language == 'de-DE':
            self.say("Ich hoffe, Du fährst nicht gerade Auto!")            
        else:
            self.say("Eu espero que voce nao esteja dirigindo agora!")
        self.complete_request()

    @register("de-DE", ".*Sag mir.*Schmutzige.*")
    @register("en-US", ".*Fale.*terra*")
    def st_dirty(self, speech, language):
        if language == 'de-DE':
            self.say("Humus. Kompost. Bims. Schlamm. Kies.")            
        else:
            self.say("Humos, Adubo, Pedra-Pome, Lama e Cascalho.")
        self.complete_request()
    

