# -*- coding: utf-8 -*-
import os
import sys
import xbmc
import sqlite3
import xbmcaddon

reload(sys)  
sys.setdefaultencoding('utf8')

class Settings():

  def __getattr__(self, name):
    temp = this.getSetting(name)
    if temp in ['true', 'True']:
      return True
    if temp in ['false', 'False']:
      return False
    if temp.isdigit():
      return int(temp)
    return temp

  def __setattr__(self, name, value):
    this.setSetting(name, str(value))
    
  
def log(msg, level = xbmc.LOGNOTICE):
  if level == xbmc.LOGERROR:
    import traceback
    xbmc.log('%s | %s' % (id, traceback.format_exc()), xbmc.LOGERROR)
  else:
    if settings.debug:
      xbmc.log("%s | %s" % (id, msg), level)

def show_progress(progress_bar, percent, msg):
  if progress_bar:
    progress_bar.update(percent, str(msg))
    log(msg)

def notify(msg):
  log("notify() %s" % msg)
  command = "Notification(%s,%s,%s)" % (translate(32003), msg, 5000)
  xbmc.executebuiltin(command) 
  
def notify_error(msg):
  log("notify_error() %s" % msg)
  command = "Notification(%s,%s,%s)" % (translate(32005), msg, 5000)
  xbmc.executebuiltin(command)  

def __update__(action, location, crash=None):
  try:
    from ga import ga
    p = {}
    p['an'] = this.getAddonInfo('name').decode('utf-8')
    p['av'] = this.getAddonInfo('version')
    p['ec'] = 'Addon actions'
    p['ea'] = action
    p['ev'] = '1'
    p['ul'] = xbmc.getLanguage()
    p['cd'] = location
    ga('UA-79422131-10').update(p, crash)
  except Exception, er:
    log(er)

def clear_session():
  try: 
    os.remove(session)
    log("Session destroyed!")
  except:
    pass

def get_template_file():
  template_file = settings.template_file
  if not os.path.isfile(template_file):
    cwd = xbmc.translatePath( this.getAddonInfo('path') ).decode('utf-8')
    template_file = os.path.join(cwd, 'resources', 'order.txt')
  return template_file

def get_disabled_groups():
  disabled_groups = []
  if settings.hide_children:
    disabled_groups.append('Детски') 
  if settings.hide_docs:
    disabled_groups.append('Документални') 
  if settings.hide_french:
    disabled_groups.append('Френски') 
  if settings.hide_english:
    disabled_groups.append('Английски') 
  if settings.hide_german:
    disabled_groups.append('Немски') 
  if settings.hide_holland:
    disabled_groups.append('Холандски') 
  if settings.hide_italian:
    disabled_groups.append('Италиански') 
  if settings.hide_movies:
    disabled_groups.append('Филми') 
  if settings.hide_music:
    disabled_groups.append('Музикални') 
  if settings.hide_news:
    disabled_groups.append('Новини') 
  if settings.hide_russian:
    disabled_groups.append('Руски') 
  if settings.hide_serbian:
    disabled_groups.append('Сръбски') 
  if settings.hide_theme:
    disabled_groups.append('Тематични') 
  if settings.hide_turkish:
    disabled_groups.append('Турски') 
  if settings.hide_xxx:
    disabled_groups.append('Възрастни') 
  if settings.hide_sports:
    disabled_groups.append('Спортни') 
  if settings.hide_bulgarian:
    disabled_groups.append('Български') 
  if settings.hide_asia:
    disabled_groups.append('Азиатски') 
  if settings.hide_others:
    disabled_groups.append('Други')
  if settings.hide_information_pr:
    disabled_groups.append('information')
  if settings.hide_movies_pr:
    disabled_groups.append('cinema')
  if settings.hide_news_pr:
    disabled_groups.append('news')
  if settings.hide_docs_pr:
    disabled_groups.append('documentary')
  if settings.hide_sports_pr:
    disabled_groups.append('sports')
  if settings.hide_entertainments_pr:
    disabled_groups.append('entertainments')
  if settings.hide_russian_pr:
    disabled_groups.append('Russian')
  if settings.hide_music_pr:
    disabled_groups.append('music')
  if settings.hide_children_pr:
    disabled_groups.append('children\'s')
  if settings.hide_xxx_pr:
    disabled_groups.append('for adults')
  if settings.hide_free_pr:
    disabled_groups.append('free web tv')    
  if settings.hide_culture_pr:
    disabled_groups.append('culture')  
    
  return disabled_groups

  
## Initialize the addon
id            = "plugin.program.tvbgpvr.backend"
this          = xbmcaddon.Addon(id=id)
translate     = this.getLocalizedString
settings      = Settings()
pl_name       = "playlist.m3u"
profile_dir   = xbmc.translatePath( this.getAddonInfo('profile') ).decode('utf-8')
db_dir        = os.path.join(profile_dir, "../../Database/")
pl_path       = os.path.join(profile_dir, pl_name)
pl_cache      = os.path.join(profile_dir, ".cache")
session       = os.path.join(profile_dir, '.session')
__version__   = xbmc.getInfoLabel("System.BuildVersion")
VERSION       = int(__version__[0:2])
user_agent    = "Kodi %s" % __version__
scheduled_run = len(sys.argv) > 1 and sys.argv[1] == str(True)

### Literals
RUNSCRIPT     = "RunScript(%s, True)" % id
GET           = 'GET'
HEAD          = 'HEAD'
LOCALHOST     = "localhost"
NEWLINE       = "\n"
STREAM_URL    = "http://localhost:%s/tvbgpvr.backend/stream/%s"

### Addon starts
if settings.firstrun:
  this.openSettings()
  settings.firstrun = False
  
__update__('operation', 'regeneration')
