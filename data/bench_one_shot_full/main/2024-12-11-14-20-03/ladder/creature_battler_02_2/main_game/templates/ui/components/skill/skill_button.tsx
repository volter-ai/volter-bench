import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { Button } from "@/components/ui/button"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ComponentPropsWithoutRef<typeof Button> {
  uid: string
  name: string
  description: string
  stats: {
    damage?: number
    accuracy?: number
    cost?: number
  }
}

let SkillButton = React.forwardRef<
  HTMLButtonElement,
  SkillButtonProps
>(({ uid, name, description, stats, ...props }, ref) => {
  return (
    <HoverCard>
      <HoverCardTrigger asChild>
        <Button
          ref={ref}
          className="w-full"
          {...props}
        >
          {name}
        </Button>
      </HoverCardTrigger>
      <HoverCardContent className="w-80">
        <div className="space-y-2">
          <h4 className="text-sm font-semibold">{name}</h4>
          <p className="text-sm">{description}</p>
          <div className="text-sm">
            {stats.damage && <div>Damage: {stats.damage}</div>}
            {stats.accuracy && <div>Accuracy: {stats.accuracy}%</div>}
            {stats.cost && <div>Cost: {stats.cost}</div>}
          </div>
        </div>
      </HoverCardContent>
    </HoverCard>
  )
})

SkillButton.displayName = "SkillButton"

SkillButton = withClickable(SkillButton)

export { SkillButton }
export type { SkillButtonProps }
