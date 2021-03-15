def scale_axes(axes,scale):
    # This function is used to scale a list of matplotlib Axis objects without changing
    # the total space taken up by those axes.
    #
    # 'axes'  1D list-like object of matplotlib Axis objects
    # 'scale' 1D list-like object that specifies how to scale the axes. Entries of
    #         'None' automatically scale the corresponding axis in the axes list based
    #         on the other list entries.
    # If you specify a row of axes, their widths will be scaled. If you specify a column
    # of axes, their heights will be scaled.
    
    if len(axes) != len(scale): raise TypeError("Both 'axes' and 'scale' must the same size")
    if len(axes) == 1 or len(scale) == 1:
        raise TypeError("Both 'axes' and 'scale' must be list-like objects with lengths > 1")
    
    poss = [a.get_position() for a in axes]
    
    # Check to see if the axes list is for a row, or for a column
    axes_is_row = False
    axes_is_col = False
    for i,p1 in enumerate(poss):
        poss2 = [p for p in poss if p is not p1]
        if not all([True if p.x0 == p1.x0 and p.x1 == p1.x1 else False for p in poss2]):
            axes_is_row = True
        if not all([True if p.y0 == p1.y0 and p.y1 == p1.y1 else False for p in poss2]):
            axes_is_col = True
    if (axes_is_row and axes_is_col) or (not axes_is_row and not axes_is_col):
        raise Exception("Could not detect whether the axes are in a row or in a column")
    
    if axes_is_row: # The axes are in a row, so scale their widths
        # Sort the axes from left-to-right
        x0s = [p.x0 for p in poss]
        idx = [x0s.index(x) for x in sorted(x0s)]
        scale = [scale[i] for i in idx]
        axes = [axes[i] for i in idx]
        widths = [p.width for p in [poss[i] for i in idx]]
        
        nones = [True if s is None else False for s in scale]
        if any(nones):
            none_widths = (sum(widths) - sum([w*s for w,s in zip(widths,scale) if s is not None]))/sum(nones)
        
        for i,(ax,s,w) in enumerate(zip(axes,scale,widths)):
            p = ax.get_position()
            if s is not None: new_width = s*w
            else: new_width = none_widths
            dw = w-new_width
            ax.set_position([p.x0,p.y0,new_width,p.height])
            for a in axes[i+1:]:
                p = a.get_position()
                a.set_position([p.x0-dw,p.y0,w,p.height])
        
    else: # The axes are in a column, so scale their heights
        # Sort the axes from left-to-right
        y0s = [p.y0 for p in poss]
        idx = [y0s.index(y) for y in sorted(y0s)]
        scale = [scale[i] for i in idx]
        axes = [axes[i] for i in idx]
        heights = [p.height for p in [poss[i] for i in idx]]
        
        nones = [True if s is None else False for s in scale]
        if any(nones):
            none_heights = (sum(heights) - sum([h*s for h,s in zip(heights,scale) if s is not None]))/sum(nones)
        
        for i,(ax,s,h) in enumerate(zip(axes,scale,heights)):
            p = ax.get_position()
            if s is not None: new_height = s*h
            else: new_height = none_heights
            dh = h-new_height
            ax.set_position([p.x0,p.y0,p.width,new_height])
            for a in axes[i+1:]:
                p = a.get_position()
                a.set_position([p.x0,p.y0-dh,p.width,p.height])