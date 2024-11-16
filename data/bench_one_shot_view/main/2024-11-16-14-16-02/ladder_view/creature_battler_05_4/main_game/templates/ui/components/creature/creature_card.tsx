import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { Card as BaseCard, CardContent as BaseCardContent, CardHeader as BaseCardHeader, CardTitle as BaseCardTitle } from "@/components/ui/card"
import { Progress as BaseProgress } from "@/components/ui/progress"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  image: string
  currentHp: number
  maxHp: number
}

let Card = withClickable(BaseCard)
let CardContent = withClickable(BaseCardContent)
let CardHeader = withClickable(BaseCardHeader)
let CardTitle = withClickable(BaseCardTitle)
let Progress = withClickable(BaseProgress)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, image, currentHp, maxHp, ...props }, ref) => {
    return (
      <Card uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`} className="flex flex-col gap-4">
          <img 
            src={image}
            alt={name}
            className="w-full h-48 object-contain"
          />
          <div className="space-y-2">
            <div className="flex justify-between">
              <span>HP</span>
              <span>{currentHp}/{maxHp}</span>
            </div>
            <Progress uid={`${uid}-progress`} value={(currentHp / maxHp) * 100} />
          </div>
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
