import * as React from "react"
import * as HoverCardPrimitive from "@radix-ui/react-hover-card"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

interface SkillHoverCardProps extends React.ComponentPropsWithoutRef<typeof HoverCardPrimitive.Root> {
  uid: string
}

let SkillHoverCardBase = React.forwardRef<
  React.ElementRef<typeof HoverCardPrimitive.Root>,
  SkillHoverCardProps
>(({ className, ...props }, ref) => (
  <HoverCardPrimitive.Root {...props} />
))

let SkillHoverCardTriggerBase = React.forwardRef<
  React.ElementRef<typeof HoverCardPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof HoverCardPrimitive.Trigger> & { uid: string }
>(({ className, ...props }, ref) => (
  <HoverCardPrimitive.Trigger ref={ref} {...props} />
))

let SkillHoverCardContentBase = React.forwardRef<
  React.ElementRef<typeof HoverCardPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof HoverCardPrimitive.Content> & { uid: string }
>(({ className, align = "center", sideOffset = 4, ...props }, ref) => (
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

SkillHoverCardBase.displayName = "SkillHoverCard"
SkillHoverCardTriggerBase.displayName = "SkillHoverCardTrigger"
SkillHoverCardContentBase.displayName = "SkillHoverCardContent"

let SkillHoverCard = withClickable(SkillHoverCardBase)
let SkillHoverCardTrigger = withClickable(SkillHoverCardTriggerBase)
let SkillHoverCardContent = withClickable(SkillHoverCardContentBase)

export { SkillHoverCard, SkillHoverCardTrigger, SkillHoverCardContent }
