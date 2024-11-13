import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { Button } from "@/components/ui/button"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ComponentProps<typeof Button> {
  uid: string
  skillName: string
  description: string
  stats: {
    damage?: number
    accuracy?: number
    [key: string]: any
  }
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, skillName, description, stats, className, ...props }, ref) => {
    return (
      <HoverCard uid={uid}>
        <HoverCardTrigger uid={uid} asChild>
          <Button ref={ref} className={className} uid={uid} {...props}>
            {skillName}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={uid} className="w-80">
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{skillName}</h4>
            <p className="text-sm">{description}</p>
            <div className="flex flex-col gap-1">
              {Object.entries(stats).map(([key, value]) => (
                <div key={key} className="flex justify-between text-sm">
                  <span className="capitalize">{key}:</span>
                  <span>{value}</span>
                </div>
              ))}
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
