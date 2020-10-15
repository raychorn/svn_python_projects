                                s_parent = None
                                for s in s_name.split(os.sep):
                                    if (len(s) == 0):
                                        continue
                                    try:
                                        r1 = Node.objects.get(name=s)
                                    except model.DoesNotExist:
                                        r1 = Node(name=s)
                                    if (not r1):
                                        try:
                                            p1 = Node.objects.get(parent=s_parent)
                                        except:
                                            p1 = None
                                        try:
                                            latest = Node.objects.latest('id')
                                        except:
                                            latest = None
                                        r1 = Node(id=1 if (latest is None) else latest,name='+++',parent=None,creation_date=_utils.timeStampLocalTime(),modification_date=_utils.timeStampLocalTime(),is_active=True,is_file=True)
                                        r1.save()
                                    s_parent = s
