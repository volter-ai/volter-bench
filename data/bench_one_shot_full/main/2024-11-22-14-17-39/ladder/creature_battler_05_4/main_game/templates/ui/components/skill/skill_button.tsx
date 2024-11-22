import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  uid: string
  skillName: string
  description: string
  stats: {
    damage?: number
    accuracy?: number
    type?: string
  }
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, className, skillName, description, stats, ...props }, ref) => {
    return (
      <HoverCard uid={`${uid}-hover`}>
        <HoverCardTrigger uid={`${uid}-trigger`} asChild>
          <Button
            uid={`${uid}-button`}
            ref={ref}
            className={cn("w-[200px]", className)}
            {...props}
          >
            {skillName}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={`${uid}-content`} className="w-80">
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{skillName}</h4>
            <p className="text-sm text-muted-foreground">
              {description}
            </p>
            <div className="flex flex-col gap-1 text-sm">
              {stats.damage && <div>Damage: {stats.damage}</div>}
              {stats.accuracy && <div>Accuracy: {stats.accuracy}%</div>}
              {stats.type && <div>Type: {stats.type}</div>}
            </div>
          </div>
        </HoverCardContent>
      </HoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"

SkillButton = withClickable(SkillButton)

export { SkillButton }
