import * as React from "react"
import * as HoverCardPrimitive from "@/components/ui/hover-card"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

let SkillButton = HoverCardPrimitive.Root

let SkillButtonTrigger = HoverCardPrimitive.Trigger

let SkillButtonContent = React.forwardRef<
  React.ElementRef<typeof HoverCardPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof HoverCardPrimitive.Content> & { uid: string }
>(({ className, align = "center", sideOffset = 4, uid, ...props }, ref) => (
  <HoverCardPrimitive.Content
    ref={ref}
    align={align}
    sideOffset={sideOffset}
    className={cn(
      "z-50 w-64 rounded-md border bg-popover p-4 text-popover-foreground shadow-md outline-none data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
      className
    )}
    {...props}
  />
))

// Set display name
SkillButtonContent.displayName = HoverCardPrimitive.Content.displayName

// Apply withClickable
SkillButton = withClickable(SkillButton)
SkillButtonTrigger = withClickable(SkillButtonTrigger)
SkillButtonContent = withClickable(SkillButtonContent)

export { SkillButton, SkillButtonTrigger, SkillButtonContent }
