/*
 * This library is part of OpenCms -
 * the Open Source Content Management System
 *
 * Copyright (c) Alkacon Software GmbH & Co. KG (http://www.alkacon.com)
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 * For further information about Alkacon Software, please see the
 * company website: http://www.alkacon.com
 *
 * For further information about OpenCms, please see the
 * project website: http://www.opencms.org
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

package org.opencms.ui.actions;

import org.opencms.file.CmsObject;
import org.opencms.file.CmsResource;
import org.opencms.gwt.shared.CmsCoreData.AdeContext;
import org.opencms.main.OpenCms;
import org.opencms.ui.I_CmsDialogContext;
import org.opencms.ui.I_CmsDialogContext.ContextType;
import org.opencms.ui.I_CmsDialogContextWithAdeContext;
import org.opencms.ui.contextmenu.CmsMenuItemVisibilityMode;
import org.opencms.ui.contextmenu.CmsStandardVisibilityCheck;
import org.opencms.ui.contextmenu.I_CmsHasMenuItemVisibility;
import org.opencms.ui.dialogs.CmsDeleteDialog;
import org.opencms.workplace.explorer.Messages;

import java.util.List;
import java.util.Map;

/**
 * The delete dialog action.<p>
 */
public class CmsDeleteDialogAction extends A_CmsWorkplaceAction implements I_CmsADEAction {

    /** The action id. */
    public static final String ACTION_ID = "delete";

    /** The action visibility. */
    public static final I_CmsHasMenuItemVisibility VISIBILITY = CmsStandardVisibilityCheck.DEFAULT;

    /** The action visibility. */
    public static final I_CmsHasMenuItemVisibility ELEMENT_AUTHOR_GALLERY_VISIBILITY = CmsStandardVisibilityCheck.DEFAULT_AUTHOR;

    /**
     * @see org.opencms.ui.actions.I_CmsWorkplaceAction#executeAction(org.opencms.ui.I_CmsDialogContext)
     */
    public void executeAction(I_CmsDialogContext context) {

        if (!hasBlockingLocks(context)) {
            openDialog(new CmsDeleteDialog(context), context);
        }
    }

    /**
     * @see org.opencms.ui.actions.I_CmsADEAction#getCommandClassName()
     */
    public String getCommandClassName() {

        return "org.opencms.gwt.client.ui.contextmenu.CmsDeleteResource";
    }

    /**
     * @see org.opencms.ui.actions.I_CmsWorkplaceAction#getId()
     */
    public String getId() {

        return ACTION_ID;
    }

    /**
     * @see org.opencms.ui.actions.I_CmsADEAction#getJspPath()
     */
    public String getJspPath() {

        return null;
    }

    /**
     * @see org.opencms.ui.actions.I_CmsADEAction#getParams()
     */
    public Map<String, String> getParams() {

        return null;
    }

    /**
     * @see org.opencms.ui.contextmenu.I_CmsHasMenuItemVisibility#getVisibility(org.opencms.file.CmsObject, java.util.List)
     */
    public CmsMenuItemVisibilityMode getVisibility(CmsObject cms, List<CmsResource> resources) {

        return VISIBILITY.getVisibility(cms, resources);
    }

    /**
     * @see org.opencms.ui.actions.A_CmsWorkplaceAction#getVisibility(org.opencms.ui.I_CmsDialogContext)
     */
    @Override
    public CmsMenuItemVisibilityMode getVisibility(I_CmsDialogContext context) {

        if (ContextType.sitemapToolbar.equals(context.getContextType())
            || ContextType.containerpageToolbar.equals(context.getContextType())) {
            return CmsMenuItemVisibilityMode.VISIBILITY_INVISIBLE;
        }

        if (context instanceof I_CmsDialogContextWithAdeContext) {
            AdeContext adeContext = ((I_CmsDialogContextWithAdeContext)context).getAdeContext();
            if (AdeContext.gallery.equals(adeContext)) {
                if (OpenCms.getWorkplaceManager().isAllowElementAuthorToWorkInGalleries()) {
                    return ELEMENT_AUTHOR_GALLERY_VISIBILITY.getVisibility(context.getCms(), context.getResources());
                }
            }
        }
        return super.getVisibility(context);
    }

    /**
     * @see org.opencms.ui.actions.I_CmsADEAction#isAdeSupported()
     */
    public boolean isAdeSupported() {

        return true;
    }

    /**
     * @see org.opencms.ui.actions.A_CmsWorkplaceAction#getDialogTitleKey()
     */
    @Override
    protected String getDialogTitleKey() {

        return org.opencms.ui.Messages.GUI_DIALOGTITLE_DELETE_0;
    }

    /**
     * @see org.opencms.ui.actions.A_CmsWorkplaceAction#getTitleKey()
     */
    @Override
    protected String getTitleKey() {

        return Messages.GUI_EXPLORER_CONTEXT_DELETE_0;
    }
}
