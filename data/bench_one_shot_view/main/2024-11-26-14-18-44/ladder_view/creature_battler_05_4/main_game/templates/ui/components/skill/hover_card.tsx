import * as React from "react"
import { HoverCard as ShadcnHoverCard, HoverCardContent as ShadcnHoverCardContent, HoverCardTrigger as ShadcnHoverCardTrigger } from "@/components/ui/hover-card"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

interface WithUid {
  uid: string
}

let HoverCard = React.forwardRef<
  React.ElementRef<typeof ShadcnHoverCard>,
  React.ComponentPropsWithoutRef<typeof ShadcnHoverCard> & WithUid
>(({ uid, ...props }, ref) => (
  <ShadcnHoverCard {...props} />
))

let HoverCardTrigger = React.forwardRef<
  React.ElementRef<typeof ShadcnHoverCardTrigger>,
  React.ComponentPropsWithoutRef<typeof ShadcnHoverCardTrigger> & WithUid
>(({ uid, ...props }, ref) => (
  <ShadcnHoverCardTrigger ref={ref} {...props} />
))

let HoverCardContent = React.forwardRef<
  React.ElementRef<typeof ShadcnHoverCardContent>,
  React.ComponentPropsWithoutRef<typeof ShadcnHoverCardContent> & WithUid
>(({ uid, className, ...props }, ref) => (
  <ShadcnHoverCardContent
    ref={ref}
    className={cn(className)}
    {...props}
  />
))

HoverCard = withClickable(HoverCard)
HoverCardTrigger = withClickable(HoverCardTrigger)
HoverCardContent = withClickable(HoverCardContent)

HoverCard.displayName = "HoverCard"
HoverCardTrigger.displayName = "HoverCardTrigger"
HoverCardContent.displayName = "HoverCardContent"

export { HoverCard, HoverCardTrigger, HoverCardContent }
