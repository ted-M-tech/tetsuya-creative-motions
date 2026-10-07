import React from 'react';
import {CaretDown} from '@phosphor-icons/react';
import './select.css';

// Native picker, form semantics and event/ref contract; shared closed-control styling.
// Layout belongs to the wrapper. Do not style its select/chevron from a feature.
export default function Select({children,className='',variant='field',fullWidth=false,ref,...props}){
 return <span className={`ui-select ui-select--${variant}${fullWidth?' ui-select--full':''}${className?' '+className:''}`}><select {...props} ref={ref}>{children}</select><CaretDown size={16} aria-hidden="true" focusable="false"/></span>;
}
