import * as React from "react"
import { cn } from "@/lib/utils"
import { Card as BaseCard, CardContent as BaseCardContent, CardHeader as BaseCardHeader, CardTitle as BaseCardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import withClickable from "@/lib/withClickable"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  image: string
  currentHp: number
  maxHp: number
}

let Card = withClickable(BaseCard)
let CardHeader = withClickable(BaseCardHeader)
let CardContent = withClickable(BaseCardContent)
let CardTitle = withClickable(BaseCardTitle)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, image, currentHp, maxHp, ...props }, ref) => {
    return (
      <Card uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <div className="flex flex-col gap-4">
            <img
              src={image}
              alt={name}
              className="h-48 w-48 object-contain mx-auto"
            />
            <Progress value={(currentHp / maxHp) * 100} />
            <div className="text-center">
              {currentHp} / {maxHp} HP
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
