import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

interface SkillHoverCardProps extends React.ComponentProps<typeof HoverCard> {
  uid: string
  skillName: string
  description: string
  stats: {
    damage?: number
    accuracy?: number
    type?: string
  }
  onSkillClick?: () => void
}

let SkillHoverCard = React.forwardRef<
  React.ElementRef<typeof HoverCard>,
  SkillHoverCardProps
>(({ uid, skillName, description, stats, onSkillClick, className, ...props }, ref) => (
  <HoverCard {...props}>
    <HoverCardTrigger asChild>
      <Button 
        uid={`${uid}-button`}
        onClick={onSkillClick}
        className={cn("w-full", className)}
      >
        {skillName}
      </Button>
    </HoverCardTrigger>
    <HoverCardContent className="w-80">
      <div className="space-y-2">
        <h4 className="font-medium leading-none">{skillName}</h4>
        <p className="text-sm text-muted-foreground">{description}</p>
        <div className="text-sm">
          {stats.damage && <div>Damage: {stats.damage}</div>}
          {stats.accuracy && <div>Accuracy: {stats.accuracy}%</div>}
          {stats.type && <div>Type: {stats.type}</div>}
        </div>
      </div>
    </HoverCardContent>
  </HoverCard>
))

SkillHoverCard.displayName = "SkillHoverCard"

SkillHoverCard = withClickable(SkillHoverCard)

export { SkillHoverCard }
