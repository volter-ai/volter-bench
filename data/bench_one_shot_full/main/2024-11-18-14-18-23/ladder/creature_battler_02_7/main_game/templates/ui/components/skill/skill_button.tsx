import * as React from "react"
import * as HoverCardPrimitive from "@radix-ui/react-hover-card"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ComponentPropsWithoutRef<typeof HoverCardPrimitive.Root> {
  uid: string
  name: string
  description: string
  stats: {
    damage?: number
    accuracy?: number
    cost?: number
  }
}

let SkillHoverCard = HoverCardPrimitive.Root
let SkillHoverCardTrigger = HoverCardPrimitive.Trigger
let SkillHoverCardContent = React.forwardRef<
  React.ElementRef<typeof HoverCardPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof HoverCardPrimitive.Content>
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

SkillHoverCardContent.displayName = HoverCardPrimitive.Content.displayName

// Apply withClickable
SkillHoverCard = withClickable(SkillHoverCard)
SkillHoverCardTrigger = withClickable(SkillHoverCardTrigger)
SkillHoverCardContent = withClickable(SkillHoverCardContent)

let SkillButton = React.forwardRef<HTMLDivElement, SkillButtonProps>(
  ({ uid, name, description, stats, className, ...props }, ref) => {
    return (
      <SkillHoverCard uid={uid} {...props}>
        <SkillHoverCardTrigger uid={uid} asChild>
          <Button
            className={cn("w-[200px]", className)}
          >
            {name}
          </Button>
        </SkillHoverCardTrigger>
        <SkillHoverCardContent uid={uid} className="w-80">
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{name}</h4>
            <p className="text-sm text-muted-foreground">
              {description}
            </p>
            <div className="flex gap-4 text-sm">
              {stats.damage && <div>Damage: {stats.damage}</div>}
              {stats.accuracy && <div>Accuracy: {stats.accuracy}%</div>}
              {stats.cost && <div>Cost: {stats.cost}</div>}
            </div>
          </div>
        </SkillHoverCardContent>
      </SkillHoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"

export { SkillButton, SkillHoverCard, SkillHoverCardTrigger, SkillHoverCardContent }
