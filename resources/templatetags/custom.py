# coding=utf-8
# auth: zhangyiling
# time: 2018/9/12 下午00:05
# description: 自定义过滤器; 官档: https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/


from django import template

register = template.Library()


@register.filter()
def get_product(product_id, product_dict):
    '''
    根据主机列表中的业务线id 取出业务线名字，达到主机列表显示业务线的目的；
    参数解释：
    <td>{{ server_list.service_id|get_product:product }}</td>
    product_id： 过滤器管道之前的值
    product_dict： 过滤器冒号之后的值
    :param product_id: 业务线id
    :param product_dict: 因为这是自己写的过滤器，所以，这必须是字典：{1: '业务线', 2：'业务线2',}
    :return: 在server_list.html中加载
    '''
    try:
        return product_dict[product_id]
    except:
        return ''
