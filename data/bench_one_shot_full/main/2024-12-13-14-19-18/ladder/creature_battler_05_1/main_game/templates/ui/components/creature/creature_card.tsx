import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { 
  Card as ShadcnCard, 
  CardContent as ShadcnCardContent, 
  CardHeader as ShadcnCardHeader, 
  CardTitle as ShadcnCardTitle 
} from "@/components/ui/card"
import { Progress as ShadcnProgress } from "@/components/ui/progress"

// Create wrapped versions that accept uid
let Card = withClickable(
  React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & {uid: string}>(
    ({uid, ...props}, ref) => <ShadcnCard ref={ref} {...props} />
  )
)

let CardContent = withClickable(
  React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & {uid: string}>(
    ({uid, ...props}, ref) => <ShadcnCardContent ref={ref} {...props} />
  )
)

let CardHeader = withClickable(
  React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & {uid: string}>(
    ({uid, ...props}, ref) => <ShadcnCardHeader ref={ref} {...props} />
  )
)

let CardTitle = withClickable(
  React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement> & {uid: string}>(
    ({uid, ...props}, ref) => <ShadcnCardTitle ref={ref} {...props} />
  )
)

let Progress = withClickable(
  React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & {uid: string; value: number}>(
    ({uid, ...props}, ref) => <ShadcnProgress ref={ref} {...props} />
  )
)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  image: string
  currentHp: number
  maxHp: number
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, image, currentHp, maxHp, ...props }, ref) => {
    return (
      <Card uid={`${uid}-card`} ref={ref} className={cn("w-[300px]", className)} {...props}>
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
