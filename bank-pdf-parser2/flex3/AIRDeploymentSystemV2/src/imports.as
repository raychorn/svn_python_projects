// ActionScript file
	import com.HAL.Alert.AlertPopUp;
	import com.HAL.controls.HtmlToolTip;
	import com.HAL.controls.ListGridCanvas;
	import com.HAL.controls.events.*;
	import com.HAL.controls.navigators.events.*;
	import com.HAL.sockets.events.*;
	import com.HAL.sockets.views.dialogs.NewFolderDialog;
	import com.HAL.utils.ArrayCollectionUtils;
	import com.HAL.utils.ArrayUtils;
	import com.HAL.utils.FileListUtils;
	import com.HAL.utils.Misc;
	import com.HAL.views.PackageContentsView;
	import com.HAL.views.PackagesView;
	import com.HAL.views.events.PackageBuilderCancelledEvent;
	 
	import flash.events.MouseEvent;
	import flash.filesystem.File;
	import flash.system.Capabilities;
	import flash.ui.ContextMenu;
	import flash.ui.ContextMenuItem;
	 
	import mx.collections.ArrayCollection;
	import mx.collections.Sort;
	import mx.collections.SortField;
	import mx.collections.XMLListCollection;
	import mx.containers.HBox;
	import mx.containers.HDividedBox;
	import mx.containers.TitleWindow;
	import mx.containers.ViewStack;
	import mx.controls.Alert;
	import mx.controls.Button;
	import mx.controls.List;
	import mx.events.*;
	import mx.managers.PopUpManager;
	import mx.managers.ToolTipManager;
	import mx.styles.CSSStyleDeclaration;
	import mx.styles.StyleManager;

	import com.HAL.controls.navigators.events.FolderNavigatorChangedEvent;
	import com.HAL.utils.FileUtils;
	import com.HAL.utils.LicenseUtils;
	import com.HAL.utils.StringUtils;
	import com.HAL.utils.XMLObjectUtils;
	import com.HAL.views.events.ArchiveBuilderAcceptedEvent;
	import com.HAL.views.events.ArchiveBuilderCheckArchiveNameEvent;
	import com.HAL.views.events.PackageBuilderAcceptedEvent;
	import com.HAL.views.events.PackageBuilderCheckPackageNameEvent;
	
	import mx.events.FlexEvent;
	import mx.events.StateChangeEvent;
