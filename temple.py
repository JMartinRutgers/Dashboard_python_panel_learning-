#!/usr/bin/env python
# coding: utf-8

# In[1]:


import panel as pn

pn.extension('tabulator', sizing_mode="stretch_width")

# In[2]:


import hvplot.pandas
import holoviews as hv

hv.extension('bokeh')


# In[3]:


def environment():
    try:
        get_ipython()
        return "notebook"
    except:
        return "server"
environment()

# In[4]:


PALETTE = ["#ff6f69", "#ffcc5c", "#88d8b0", ]
pn.Row(
    pn.layout.HSpacer(height=50, background=PALETTE[0]),
    pn.layout.HSpacer(height=50, background=PALETTE[1]),
    pn.layout.HSpacer(height=50, background=PALETTE[2]),
)

# In[5]:


from bokeh.sampledata.autompg import autompg_clean as df
df.head()


# In[6]:


(
    df[
        (df.cyl == 4) & 
        (df.mfr.isin(['ford','chevrolet']))
    ]
    .groupby(['origin', 'cyl', 'mfr', 'yr'])['hp'].mean()
    .to_frame()
    .reset_index()
    .sort_values(by='yr')
).head(1)

# In[7]:


idf = df.interactive()

# In[8]:


cylinders = pn.widgets.IntSlider(name='Cylinders', start=4, end=8, step=2)
mfr = pn.widgets.ToggleGroup(
    name='MFR',
    options=['ford', 'chevrolet', 'honda', 'toyota', 'audi'], 
    value=['ford', 'chevrolet', 'honda', 'toyota', 'audi'],
    button_type='success')
yaxis = pn.widgets.RadioButtonGroup(
    name='Y axis', 
    options=['hp', 'weight'],
    button_type='success'
)

# In[9]:


ipipeline = (
    idf[
        (idf.cyl == cylinders) & 
        (idf.mfr.isin(mfr))
    ]
    .groupby(['origin', 'mpg'])[yaxis].mean()
    .to_frame()
    .reset_index()
    .sort_values(by='mpg')  
    .reset_index(drop=True)
)
ipipeline.head()

# In[10]:


if environment()=="server":
   theme="fast"
else:
   theme="simple"


# In[11]:


itable = ipipeline.pipe(pn.widgets.Tabulator, pagination='remote', page_size=10, theme=theme)
itable

# In[12]:


ihvplot = ipipeline.hvplot(x='mpg', y=yaxis, by='origin', color=PALETTE, line_width=6, height=400)
ihvplot


# In[13]:


template = pn.template.FastListTemplate(
    title='Interactive DataFrame Dashboards with hvplot .interactive', 
    sidebar=[cylinders, 'Manufacturers', mfr, 'Y axis' , yaxis],
    main=[ihvplot.panel(), itable.panel()],
    accent_base_color="#88d8b0",
    header_background="#88d8b0",
)
# template.show()
template.servable();

# In[ ]:



