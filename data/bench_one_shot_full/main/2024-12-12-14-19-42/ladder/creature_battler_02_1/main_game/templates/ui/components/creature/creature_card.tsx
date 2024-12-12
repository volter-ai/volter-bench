import * as React from "react"
import { cn } from "@/lib/utils"
import { 
  Card, 
  CardContent, 
  CardHeader, 
  CardTitle 
} from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import withClickable from "@/lib/withClickable"

interface CreatureProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  value?: number
}

let CreatureProgress = React.forwardRef<HTMLDivElement, CreatureProgressProps>(
  ({ uid, ...props }, ref) => (
    <Progress {...props} ref={ref} />
  )
)

CreatureProgress.displayName = "CreatureProgress"
CreatureProgress = withClickable(CreatureProgress)

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
      <Card uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
          <CreatureProgress 
            uid={`${uid}-progress`} 
            value={(hp / maxHp) * 100} 
            className="w-full" 
          />
          <div className="text-sm text-muted-foreground">
            {hp} / {maxHp} HP
          </div>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-contain"
          />
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
