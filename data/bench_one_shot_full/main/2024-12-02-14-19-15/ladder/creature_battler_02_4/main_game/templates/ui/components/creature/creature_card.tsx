import * as React from "react"
import { cn } from "@/lib/utils"
import { 
  Card as BaseCard, 
  CardContent as BaseCardContent, 
  CardHeader as BaseCardHeader, 
  CardTitle as BaseCardTitle 
} from "@/components/ui/card"
import { Progress as BaseProgress } from "@/components/ui/progress"
import withClickable from "@/lib/withClickable"

let Progress = withClickable(BaseProgress)
let Card = withClickable(BaseCard)
let CardContent = withClickable(BaseCardContent)
let CardHeader = withClickable(BaseCardHeader)
let CardTitle = withClickable(BaseCardTitle)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <Card uid={`${uid}-card`} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <img 
            src={imageUrl}
            alt={name}
            className="w-full h-48 object-contain mb-4"
          />
          <div className="space-y-2">
            <div className="flex justify-between">
              <span>HP</span>
              <span>{hp}/{maxHp}</span>
            </div>
            <Progress uid={`${uid}-progress`} value={(hp / maxHp) * 100} />
          </div>
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
